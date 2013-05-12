from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'swipe_foursquare.views.login', name='login'),
    url(r'^oauth-redirect/$', 'swipe_foursquare.views.oauth_redirect', name='oauth-redirect'),
    url(r'^admin/', include(admin.site.urls)),
)
