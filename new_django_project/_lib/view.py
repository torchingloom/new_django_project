import json
from django.core import serializers
from django.http import HttpResponse


class JSONResponseMixin(object):
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(self.convert_context_to_json(context), **response_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)


class JSONResponseMixinList(JSONResponseMixin):
    def convert_context_to_json(self, context):
        try:
            extra = context['object_list'][0].serialize_extra()
            return serializers.serialize('json', context['object_list'], **extra)
        except:
            try:
                return json.dumps(context)
            except:
                return json.dumps({})


class JSONResponseMixinDetail(JSONResponseMixin):
    def convert_context_to_json(self, context):
        serializers.serialize('json', context['object_list'])



from functools import wraps
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect


def permanent_redirect(url):
    """
    Executes a HTTP 301 (permanent) redirect after the view finishes processing. If a
    value is returned, it is ignored. Allows for the view url to be callable so the
    reverse() lookup can be used.

    @permanent_redirect('/another-url/')
    def redirect_view(request):
        ...

    @redirect(lambda: reverse('some_viewname'))
    def do_redirect(request):
        ...

    """
    def outer(f):
        @wraps(f)
        def inner(request, *args, **kwargs):
            f(request, *args, **kwargs)
            return HttpResponsePermanentRedirect(url if not callable(url) else url())
        return inner
    return outer


def redirect(url):
    """
    Executes a HTTP 302 redirect after the view finishes processing. If a value is
    returned, it is ignored. Allows for the view url to be callable so the
    reverse() lookup can be used.

    @redirect('http://www.google.com/')
    def goto_google(request):
        pass

    @redirect(lambda: reverse('some_viewname'))
    def do_redirect(request):
        ...

    """
    def outer(f):
        @wraps(f)
        def inner(request, *args, **kwargs):
            f(request, *args, **kwargs)
            return HttpResponseRedirect(url if not callable(url) else url())
        return inner
    return outer


from django.utils.decorators import available_attrs


def redirect_if_cond(test_func, url):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            return HttpResponseRedirect(url if not callable(url) else url())
        return _wrapped_view
    return decorator


def site_url():
    from django.conf import settings
    from django.contrib.sites.models import Site
    current_site = Site.objects.get_current()
    protocol = getattr(settings, 'MY_SITE_PROTOCOL', 'http')
    port = getattr(settings, 'MY_SITE_PORT', '')
    url = '%s://%s' % (protocol, current_site.domain)
    return url
