from django.shortcuts import redirect

from . import models


def login(request):
    return redirect(request.foursquare.oauth.auth_url())


def oauth_redirect(request):
    access_token = request.foursquare.oauth.get_token(request.GET['code'])
    request.foursquare.set_access_token(access_token)
    user = request.foursquare.users()
    user = models.FoursquareUser.save_token(int(user['user']['id']), access_token)
    request.session['foursquare_user_id'] = user.user_id
    return redirect('/')
