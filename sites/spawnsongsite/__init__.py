from __future__ import absolute_import

from .celery import app as celery_app

from django.contrib import admin

admin_site = admin.AdminSite()
