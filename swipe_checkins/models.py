from django.db import models
from django.dispatch import receiver


class Checkin(models.Model):
    from_number = models.CharField(max_length=40, db_index=True)
    rfid = models.CharField(max_length=40, db_index=True)
    created = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    device_number = models.CharField(max_length=40, db_index=True)
    venue_id = models.CharField(max_length=40, db_index=True)


class UserRFID(models.Model):
    user = models.ForeignKey('swipe_foursquare.FoursquareUser',
                             related_name='rfids')
    rfid = models.CharField(max_length=40, db_index=True)


@receiver(models.signals.post_save)
def push_checkin_signal(sender, instance, created, raw, using, *args, **kwargs):
    push_foursquare_checkin(instance)


def push_foursquare_checkin(checkin):
    location = Location.objects.get(device_number=checkin.from_number)
    user_rfid = UserRFID.objects.get(rfid=checkin.rfid)
    user = user_rfid.user
    client = user.get_foursquare_client()
    return client.checkins.add(venue=location.venue_id)
