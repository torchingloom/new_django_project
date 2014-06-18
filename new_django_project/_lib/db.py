# coding: utf-8

import os
import json

from django.conf import settings
from django.db import connection, transaction
from django.db.models import Model, get_app
from unidecode import unidecode
from django import forms
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PropertyDictMixin(object):
    def get_property_dict(self):
        if isinstance(self, Model):
            d = {}
            for f in self._meta.fields:
                d.update({f.name: unidecode(unicode(getattr(self, f.name)))})
            return d
        return self.__dict__


def load_customized_sql(**kwargs_parent):
    def run_sql_from_file(**kwargs):
        app = get_app(kwargs.get('app'))
        app_dir = os.path.normpath(os.path.join(os.path.dirname(app.__file__), 'sql'))
        if os.path.basename(app.__file__).find('__init__') == 0:
            app_dir = os.path.normpath(os.path.join(os.path.dirname(app.__file__), '..', 'sql'))
        name = kwargs_parent.get('name', 'custom')
        custom_files = [
            os.path.join(app_dir, "%s.%s.sql" % (name, settings.DATABASE_ENGINE)),
            os.path.join(app_dir, "%s.sql" % name)
        ]
        for custom_file in custom_files:
            if os.path.exists(custom_file):
                print "Loading SQL for %s from '%s'" % (app.__name__, os.path.basename(custom_file))
                sql = open(custom_file, 'U').read().decode("utf-8-sig").encode('utf-8')
                cursor = connection.cursor()
                try:
                    cursor.execute(sql)
                except Exception, e:
                    print "Couldn't execute SQL for %s from %s" % (app.__name__, os.path.basename(custom_file))
                    import traceback
                    traceback.print_exc()
                    transaction.rollback_unless_managed()
                else:
                    transaction.commit_unless_managed()
    return run_sql_from_file


class DictionaryField(models.Field):
    description = _("Dictionary object")

    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        if value is None:
            return None
        elif value == "":
            return {}
        elif isinstance(value, basestring):
            try:
                return dict(json.loads(value))
            except (ValueError, TypeError):
                raise exceptions.ValidationError(self.error_messages['invalid'])

        if isinstance(value, dict):
            return value
        else:
            return {}

    def get_prep_value(self, value):
        if not value:
            return ""
        elif isinstance(value, basestring):
            return value
        else:
            return json.dumps(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def clean(self, value, model_instance):
        value = super(DictionaryField, self).clean(value, model_instance)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'widget': forms.Textarea}
        defaults.update(kwargs)
        return super(DictionaryField, self).formfield(**defaults)


def vacuum_full():
    import sys
    PSQL_PATH = ''
    try:
        from settings import PSQL_PATH
    except:
        pass
    if not PSQL_PATH:
        symscnt = 80
        bordersym = '*'
        sys.stdout.write('\n\n\n%s\n%s%s%s' % (bordersym * symscnt, bordersym, ' ' * (symscnt - 2), bordersym))
        for msg in ('`PSQL_PATH` has no value!', 'Please, set it & try again, baby'):
            bats = (symscnt - msg.__len__()) / 2 - 1
            sys.stdout.write('%s%s%s%s%s' % (bordersym, ' ' * bats, msg, ' ' * bats, bordersym))
        sys.stdout.write('%s%s%s\n%s\n\n' % (bordersym, ' ' * (symscnt - 2), bordersym, bordersym * symscnt))
        return
    from settings import DATABASES
    cmd = "%s -U %s -c 'VACUUM FULL' %s" % (PSQL_PATH, DATABASES['default']['USER'], DATABASES['default']['NAME'])
    sys.stdout.write('\nExec `%s`\n' % cmd)
    os.system(cmd)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^.*?\.DictionaryField"])
except ImportError:
    pass