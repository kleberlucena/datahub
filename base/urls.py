from django.urls import path

from .views import *

app_name = 'base'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('health_check', health_check, name='health_check'),
    path('about', AboutView.as_view(), name='about'),
    # TODO: Inserir robots.txt
]