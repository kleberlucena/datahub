from django.urls import path

from .views import *

app_name = 'base'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('health_check', health_check, name='health_check'),
    path('about', AboutView.as_view(), name='about'),
    path('about', AboutView.as_view(), name='about'),
    path('authorization_error_view', authorization_error_view, name='authorization_error_view'),
    # TODO: Inserir robots.txt
]