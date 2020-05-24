# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/admin """

from django.contrib import admin

from .models import Image, Project, Software, Job, JobError


admin.site.register(Image)
admin.site.register(Project)
admin.site.register(Software)
admin.site.register(Job)
admin.site.register(JobError)
