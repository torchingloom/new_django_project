# coding: utf-8

from django.db.models.query import QuerySet
from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, blank=True,
                                        null=True, db_column='created_at')
    edited_time = models.DateTimeField(auto_now=True, blank=True, null=True,
                                       db_column='updated_at')

    class Meta:
        abstract = True

    def as_dict(self):
        raise NotImplementedError("as_dict() method for %s isn't implemented" %
                                  self.__class__.__name__)


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(is_deleted=True)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def deleted(self):
        return self.filter(is_deleted=True)

    def active(self):
        return self.exclude(is_deleted=False)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.active_only = kwargs.pop('active_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_query_set(self):
        if self.active_only:
            return SoftDeletionQuerySet(self.model).filter(is_deleted=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class BaseSoftDeletionModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(active_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super(BaseSoftDeletionModel, self).delete()


class SoftDeletionModel(BaseSoftDeletionModel):
    class Meta:
        abstract = True
