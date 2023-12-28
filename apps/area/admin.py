from django.contrib import admin
from .models import *
from apps.area import models



admin.site.register(models.Area)
