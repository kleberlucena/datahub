from django.urls import include, path
from global_login_required import login_not_required
from rest_framework import routers

from .views import *
from .api import viewsets

app_name = 'apps.person'

router = routers.DefaultRouter()

router.register(r'', viewsets.PersonViewSet)

urlpatterns = [
    path('api/v1/<uuid:uuid>/', login_not_required(viewsets.PersonRetrieve.as_view()), name='retrieve_json'),
    path('api/v1/', include(router.urls)),
]
