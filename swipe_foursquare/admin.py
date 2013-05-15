from django.contrib import admin

from . import models


class FoursquareUserAdmin(admin.ModelAdmin):
    list_display = ('user_id',)
admin.site.register(models.FoursquareUser)
