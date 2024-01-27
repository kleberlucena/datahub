from django.contrib import admin
from .models import *
from apps.protect_network import models



admin.site.register(models.Tag)
#admin.site.register(models.SpotType)
admin.site.register(models.ContactInfo)
admin.site.register(models.Spot)
admin.site.register(models.SpotAddresses)
admin.site.register(models.OpeningHours)
admin.site.register(models.Network)
admin.site.register(models.NetworkResponsible)
admin.site.register(models.Qpp)
admin.site.register(models.SecuritySurvey)
