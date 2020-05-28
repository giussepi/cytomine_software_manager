# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/tasks """

from __future__ import absolute_import, unicode_literals
import subprocess

from celery import shared_task
from celery.utils.log import get_task_logger

from cytomine_softwares.models import Job, JobError


logger = get_task_logger(__name__)


@shared_task
def execute_cytomine_software_task(command, job_id):
    """
    * Executes the command
    * If there is an error, stores the error logs as a JobError object

    Args:
        command (str): command to run the cytomine software through the docker container
        job_id  (int): ID of the Job
    """
    logger.info('execute_cytomine_software_task JOB_ID {}'.format(job_id))
    assert isinstance(command, str)
    assert isinstance(job_id, int)

    instance = Job.objects.get(id=job_id)

    # This means that when running the command something happened and the task was
    # re-scheduled. The most likely outcome is that docker ran smoothly and the
    # broker got disconnected for a while. So the admin only need to verify this
    # on Cytomine interface and create a new job with the same data in case
    # it failed
    if instance.in_progress() or instance.set_need_verification():
        # we are avoiding calling the command again in case the task with this
        # job_id is called more than one time
        if instance.in_progress():
            instance.set_need_verification()
            logger.warning('Task already have in_progress status (called twice)')
        else:
            logger.critical('Task called more than two times. status = need_verification')
        return

    instance.set_in_progress()
    # we are deleting this instance because the task could take hours; so we do not
    # want to keep an outdated instance in memory that latter could override
    # the values wrongly
    del instance

    result = subprocess.run(
        command, shell=True, check=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, universal_newlines=True
    )

    instance = Job.objects.get(id=job_id)
    if result.returncode == 0:
        # everything was OK
        instance.set_as_completed()
        return

    error = JobError.objects.create(
        return_code=str(result.returncode),
        args=str(result.args),
        stderr=result.stderr,
        stdout=result.stdout
    )
    instance.set_failed(error)
