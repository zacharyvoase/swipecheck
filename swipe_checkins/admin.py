from django.contrib import admin

from . import models


class CheckinAdmin(admin.ModelAdmin):
    list_display = ('from_number', 'rfid', 'created')
admin.site.register(models.Checkin, CheckinAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('device_number', 'venue_id')
admin.site.register(models.Location, LocationAdmin)

class UserRFID(admin.ModelAdmin):
    list_display = ('user', 'rfid')
admin.site.register(models.UserRFID)
