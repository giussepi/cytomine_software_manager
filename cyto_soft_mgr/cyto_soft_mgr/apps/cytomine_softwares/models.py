# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/models  """

from django.db import models

from core.models import BaseLog
from cytomine_softwares.constants import JobStatus


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


class JobError(BaseLog):
    """ Holds details of erros raised when executing a Job through Cytomine """
    return_code = models.CharField(max_length=60)
    args = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    # stdout = models.TextField(blank=True)

    def __str__(self):
        """ Returns the string object representation """
        return str(self.pk)


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
    status = models.CharField(
        max_length=1, choices=JobStatus.CHOICES, default=JobStatus.NOT_STARTED)
    error = models.OneToOneField('JobError', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        """ Returns the string object representation """
        return '{}-{}-{}-{}'.format(
            self.cyto_image_id, self.project, self.software, self.image)

    def update_status(self, new_status):
        """
        Updates the status

        Args:
            new_status (str): new JobStatus
        """
        assert isinstance(new_status, str)
        assert new_status in [i[0] for i in JobStatus.CHOICES]

        if self.status != new_status:
            self.status = new_status
            self.save()

    def set_in_progress(self):
        """ Sets the status to in progress """
        self.update_status(JobStatus.IN_PROGRESS)

    def set_as_completed(self):
        """ Sets the status to completed """
        self.update_status(JobStatus.COMPLETED)

    def set_failed(self, error=None):
        """
        Sets the status to Failed
        Args:
            error (JobError): JobError instance
        """
        if error is not None:
            assert isinstance(error, JobError)

        self.error = error
        self.update_status(JobStatus.FAILED)
