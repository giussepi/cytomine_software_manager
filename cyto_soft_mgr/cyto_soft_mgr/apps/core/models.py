# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/core/models """

from django.db import models


class BaseLog(models.Model):
    """ Holds basis attributes for logging """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """ meta class definitions """
        abstract = True
