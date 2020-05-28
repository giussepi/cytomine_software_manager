# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/constants """


class JobStatus:
    """ Holds the options for Job objects """
    NOT_STARTED = '0'
    COMPLETED = '1'
    IN_PROGRESS = '2'
    FAILED = '3'
    NEED_VERIFICATION = '4'

    CHOICES = (
        (NOT_STARTED, 'Not started'),
        (COMPLETED, 'Completed'),
        (IN_PROGRESS, 'In progress'),
        (FAILED, 'Failed'),
        (NEED_VERIFICATION, 'Needs verification')
    )
