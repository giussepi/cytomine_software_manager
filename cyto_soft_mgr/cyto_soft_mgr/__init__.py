# -*- coding: utf-8 -*-
""" cyto_soft_mgr/__init__ """

from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from cyto_soft_mgr.config.celery import app as celery_app

__all__ = ('celery_app',)
