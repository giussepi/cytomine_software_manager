# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/signals """

import subprocess

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from cytomine_softwares.models import Job, JobError


@receiver(post_save, sender=Job, dispatch_uid='cytomine_softwares.job.excecute_cytomine_software')
def excecute_cytomine_software(sender, **kwargs):
    """
    * Runs the job on cytomine
    * If there's an error during the execution, then the details are saved at a JobError instance
    """
    if kwargs.get('created'):
        # render the appropriate command
        instance = Job.objects.get(id=kwargs.get('instance').id)
        data = {
            'docker_image': instance.image.image,
            'cytomine_host': settings.CYTOMINE_HOST,
            'cytomine_public_key': settings.CYTOMINE_PUBLIC_KEY,
            'cytomine_private_key': settings.CYTOMINE_PRIVATE_KEY,
            'cytomine_id_project': instance.project.cyto_id,
            'cytomine_id_image_instance': instance.cyto_image_id,
            'cytomine_id_software': instance.software.cyto_id
        }
        command = render_to_string('cytomine_softwares/docker_cytomine_shell_command.tpl', data)

        # execute the command
        # TODO: replace with command only when ready to test on Desktop!b
        result = subprocess.run(
            'docker ps'.split(), shell=False, check=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, universal_newlines=True
        )
        # result = subprocess.run('ls -shal'.split(), shell=False, check=False, stdout=subprocess.PIPE,
        #                         stderr=subprocess.PIPE, universal_newlines=True)

        if result.returncode == 0:
            # everything was OK
            return

        error = JobError.objects.create(
            return_code=str(result.returncode),
            args=str(result.args),
            stderr=result.stderr,
            # stdout=result.stdout
        )
        instance.error = error
        instance.save()
