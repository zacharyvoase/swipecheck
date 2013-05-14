from django.conf import settings
from django.core.urlresolvers import reverse
import foursquare
import requests
import urlobject

from . import models


def make_request(url, headers={}, data=None):
    if data:
        response = requests.post(url, data=data, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    return foursquare._check_response(response.json())
foursquare._request_with_retry = make_request


class FoursquareUserMiddleware(object):
    def process_request(self, request):
        request.foursquare = get_foursquare_client(request)
        request.foursquare.is_authenticated = bool(request.foursquare.base_requester.oauth_token)


def get_foursquare_client(request):
    client = foursquare.Foursquare(
        client_id=settings.FOURSQUARE_CLIENT_ID,
        client_secret=settings.FOURSQUARE_CLIENT_SECRET,
        redirect_uri=get_redirect_uri(request),
        version=settings.FOURSQUARE_API_VERSION)
    client.user = None
    user_id = request.session.get('foursquare_user_id')
    if user_id:
        try:
            oauth_token_record = models.FoursquareUser.objects.get(user_id=int(user_id))
        except models.FoursquareUser.DoesNotExist:
            del request.session['foursquare_user_id']
        else:
            client.set_access_token(oauth_token_record.oauth_token)
            client.user = oauth_token_record
    return client


def get_redirect_uri(request):
    return (urlobject.URLObject('http://localhost/')
            .with_netloc(request.get_host())
            .with_path(reverse('swipe_foursquare.views.oauth_redirect')))
