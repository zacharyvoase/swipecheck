from django.db import models


class FoursquareUser(models.Model):
    user_id = models.PositiveIntegerField(db_index=True, unique=True)
    oauth_token = models.CharField(max_length=255)

    @classmethod
    def save_token(cls, user_id, oauth_token):
        user, created = cls.objects.get_or_create(
            user_id=user_id, defaults={'oauth_token': oauth_token})
        if not created:
            user.oauth_token = oauth_token
            user.save()
        return user
