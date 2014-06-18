import logging
from new import instancemethod
from threading import local

from django.conf import settings

USER_ATTR_NAME = getattr(settings, 'LOCAL_USER_ATTR_NAME', '_current_user')

_thread_locals = local()


def _do_set_current_request(request):
    setattr(_thread_locals, 'request', request)


def _do_set_current_user(user_fun):
    setattr(_thread_locals, USER_ATTR_NAME, instancemethod(user_fun, _thread_locals, type(_thread_locals)))


def get_request():
    return getattr(_thread_locals, 'request', None)


def get_current_user():
    current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
    return current_user() if current_user else current_user


class RequestMiddleware(object):
    def process_request(self, request):
        _do_set_current_request(request)
        _do_set_current_user(lambda self: getattr(request, 'user', None))