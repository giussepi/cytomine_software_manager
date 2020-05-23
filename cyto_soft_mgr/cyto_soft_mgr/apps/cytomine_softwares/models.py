# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/models  """

from django.db import models

from core.models import BaseLog


class Image(BaseLog):
    """ Holds docker image name """
    image = models.CharField(max_length=120, help_text='Docker image name')

    class Meta:
        """ Meta class definitions """
        verbose_name = 'Docker Image'
        verbose_name_plural = 'Docker Images'

    def __str__(self):
        """ Returns the string object representation """
        return str(self.image)


class Project(BaseLog):
    """ Holds Cytomine projects data """
    cyto_id = models.IntegerField('ID', help_text='Project ID in Cytomine')

    def __str__(self):
        """ Returns the string object representation """
        return str(self.cyto_id)


class Software(BaseLog):
    """ Holds Cytomine softwares data """
    cyto_id = models.IntegerField('ID', help_text='Sofware ID in Cytomine')

    def __str__(self):
        """ Returns the string object representation """
        return str(self.cyto_id)


class Job(BaseLog):
    """ Hold data from cytomine jobs excecuted """
    cyto_image_id = models.IntegerField(
        'Image ID',
        help_text='Image ID in Cytomine'
    )
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    software = models.ForeignKey('Software', on_delete=models.CASCADE)
    image = models.ForeignKey(
        'Image', on_delete=models.CASCADE, verbose_name='Docker Image name')

    def __str__(self):
        """ Returns the string object representation """
        return '{}-{}-{}-{}'.format(
            self.cyto_image_id, self.project, self.software, self.image)
