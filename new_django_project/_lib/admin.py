# coding: utf-8

from django.contrib import admin


class SoftDeletionModelAdmin(admin.ModelAdmin):
    exclude = ['is_deleted']
