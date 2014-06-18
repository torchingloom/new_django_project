# coding: utf-8

from south.signals import post_migrate, pre_migrate

from new_django_project._lib.db import load_customized_sql

pre_migrate.connect(load_customized_sql(name='pre_migrate'), weak=False)
post_migrate.connect(load_customized_sql(name='post_migrate'), weak=False)
