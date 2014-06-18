# coding: utf-8
from django.conf import settings
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from new_django_project._lib.models import SoftDeletionModel

