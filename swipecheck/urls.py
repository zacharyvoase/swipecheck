from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', 'swipe_checkins.views.list_rfids', name='list_rfids'),
    url(r'^delete-rfid/$', 'swipe_checkins.views.delete_rfid', name='delete_rfid'),
    url(r'^login/$', 'swipe_foursquare.views.login', name='login'),
    url(r'^oauth-redirect/$', 'swipe_foursquare.views.oauth_redirect', name='oauth-redirect'),
    url(r'^sms/$', 'swipe_checkins.views.sms_received', name='twilio-sms'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
)
