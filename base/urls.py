from django.urls import path
from global_login_required import login_not_required

from .views import *

app_name = 'base'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('health_check', health_check, name='health_check'),
    path('about', AboutView.as_view(), name='about'),
]