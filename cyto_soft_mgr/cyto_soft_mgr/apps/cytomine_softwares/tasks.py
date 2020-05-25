# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/tasks """

from __future__ import absolute_import, unicode_literals
import subprocess

from celery import shared_task

from cytomine_softwares.models import Job, JobError


@shared_task
def execute_cytomine_software_task(command, job_id):
    """
    * Executes the command
    * If there is an error, stores the error logs as a JobError object

    Args:
        command (str): command to run the cytomine software through the docker container
        job_id  (int): ID of the Job
    """
    assert isinstance(command, str)
    assert isinstance(job_id, int)

    instance = Job.objects.get(id=job_id)
    instance.set_in_progress()
    # we are deleting this instance because the task could take hours; so we do not
    # want to keep an outdated instance in memory that latter could override
    # the values wrongly
    del instance

    # TODO: replace with command only when ready to test on Desktop!
    result = subprocess.run(
        'docker ps'.split(), shell=False, check=False, stdout=subprocess.PIPE,
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
        # stdout=result.stdout
    )
    instance.set_failed(error)
