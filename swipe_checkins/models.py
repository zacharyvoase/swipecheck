from django.db import models


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
