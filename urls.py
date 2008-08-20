import os

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^patchrobot/', include('patchrobot.foo.urls')),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/issues/'}),
    (r'^admin/(.*)', admin.site.root),
    (r'^issues/$', 'patchrobot.review.views.index'),
    (r'^issues/(?P<patch_id>\d+)/$', 'patchrobot.review.views.patch'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')})
)
