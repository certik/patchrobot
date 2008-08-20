from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^patchrobot/', include('patchrobot.foo.urls')),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^issues/$', 'patchrobot.review.views.index'),
    (r'^issues/(?P<issue_id>\d+)/$', 'patchrobot.review.views.issue'),
    (r'^issues/(?P<issue_id>\d+)/(?P<message_id>\d+)/$',
        'patchrobot.review.views.message'),
)
