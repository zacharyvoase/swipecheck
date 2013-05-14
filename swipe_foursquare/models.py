from django.conf import settings
from django.db import models
import foursquare


class FoursquareUser(models.Model):
    user_id = models.PositiveIntegerField(db_index=True, unique=True)
    oauth_token = models.CharField(max_length=255)

    def get_foursquare_client(self):
        client = foursquare.Foursquare(version=settings.FOURSQUARE_API_VERSION)
        client.user = self
        client.set_access_token(self.oauth_token)
        return client

    @classmethod
    def save_token(cls, user_id, oauth_token):
        user, created = cls.objects.get_or_create(
            user_id=user_id, defaults={'oauth_token': oauth_token})
        if not created:
            user.oauth_token = oauth_token
            user.save()
        return user
