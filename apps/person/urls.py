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
    path('api/v1/<uuid:uuid>/face/', login_not_required(viewsets.PersonAddFaceView.as_view()), name='add_face_json'),
    path('api/v1/<uuid:uuid>/tatoo/', login_not_required(viewsets.PersonAddTatooView.as_view()), name='add_tatoo_json'),
    path('api/v1/<uuid:uuid>/nickname/', login_not_required(viewsets.PersonAddNicknameView.as_view()), name='add_nickname_json'),
    path('api/v1/<uuid:uuid>/physical/', login_not_required(viewsets.PersonAddPhysicalView.as_view()), name='add_physical_json'),
    path('api/v1/<uuid:uuid>/document/', login_not_required(viewsets.PersonAddDocumentView.as_view()), name='add_document_json'),
    path('api/v1/<uuid:uuid>/address/', login_not_required(viewsets.PersonAddAddressView.as_view()), name='add_address_json'),
    path('api/v1/', include(router.urls)),
]
