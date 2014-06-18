# coding: utf-8


def instance_dict(instance, key_format=None):
   "Returns a dictionary containing field names and values for the given instance"
   from django.db.models.fields.related import ForeignKey
   if key_format:
       assert '%s' in key_format, 'key_format must contain a %s'
   key = lambda key: key_format and key_format % key or key

   d = {}
   for field in instance._meta.fields:
       attr = field.name
       value = getattr(instance, attr)
       if value is not None and isinstance(field, ForeignKey):
           value = value._get_pk_val()
       d[key(attr)] = value
   for field in instance._meta.many_to_many:
       d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
   return d


def pluralize(value, arg=u"один,два,ноль/много"):
    args = arg.split(",")
    if not value:
       return args[2]
    number = abs(int(value))
    a = number % 10
    b = number % 100
    if (a == 1) and (b != 11):
        return args[0]
    elif (a > 1) and (a < 5) and ((b < 10) or (b > 20)):
        return args[1]
    else:
        return args[2]