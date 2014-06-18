# coding: utf-8

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns('',
        (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico'))
    )

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^secretzone/', include(admin.site.urls)),

    (r'^tinymce/', include('tinymce.urls')),
)
