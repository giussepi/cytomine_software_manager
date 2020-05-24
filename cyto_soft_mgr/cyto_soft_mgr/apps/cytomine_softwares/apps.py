# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/apps """

from django.apps import AppConfig


class CytomineSoftwaresConfig(AppConfig):
    name = 'cytomine_softwares'

    def ready(self):
        """ Registration of signals """
        from cytomine_softwares import signals
