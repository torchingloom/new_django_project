# coding: utf-8

from django.contrib import admin
from django.contrib.sites.models import Site
from new_django_project._lib.admin import SoftDeletionModelAdmin

admin.site.unregister(Site)

