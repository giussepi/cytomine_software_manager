# -*- coding: utf-8 -*-
""" cyto_soft_mgr/apps/cytomine_softwares/admin """

from django.contrib.auth.models import User, Group
from django.contrib import admin

from cytomine_softwares.models import Image, Project, Software, Job, JobError


admin.site.register(Image)
admin.site.register(JobError)
admin.site.register(Project)
admin.site.register(Software)

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """ Job ModelAdmin """
    list_display = ('__str__', 'status')
    list_filter = ('status',)
    date_hierarchy = 'created'
