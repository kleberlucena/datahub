from django.contrib import admin
from .models import *
from apps.area import models



admin.site.register(models.Area)
# admin.site.register(models.Qpp)
# admin.site.register(models.Cpr)
