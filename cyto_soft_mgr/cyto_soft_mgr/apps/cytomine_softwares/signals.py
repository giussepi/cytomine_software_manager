# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/signals """

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from cytomine_softwares.models import Job
from cytomine_softwares.tasks import execute_cytomine_software_task


@receiver(post_save, sender=Job, dispatch_uid='cytomine_softwares.job.excecute_cytomine_software')
def execute_cytomine_software(sender, **kwargs):
    """ Runs the job on cytomine though Celery """
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

        # execute the command asynchronously via Celery
        execute_cytomine_software_task.apply_async(args=(command, instance.id))
