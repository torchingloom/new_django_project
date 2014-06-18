# coding: utf-8

from django.contrib.auth.models import UserManager as __UserManager, AbstractUser
from django.db import models


class UserManager(__UserManager):
    pass


class User(AbstractUser):
    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

    def __unicode__(self):
        return u'%s' % self.get_full_name()
