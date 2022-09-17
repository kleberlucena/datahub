from django.urls import include, path
from global_login_required import login_not_required

from . import viewsets

app_name = 'apps.person.legacy'

urlpatterns = [
    path('<str:username>/', viewsets.AddPersonView.as_view(), name='add_legacy_person_json'),
    path('<uuid:uuid>/face/<str:username>/', viewsets.PersonAddFaceView.as_view(), name='add_legacy_face_json'),
    path('<uuid:uuid>/address/<str:username>/', viewsets.PersonAddAddressView.as_view(), name='add_legacy_address_json'),
    path('<uuid:uuid>/image/<str:username>/', viewsets.PersonAddImageView.as_view(), name='add_legacy_image_json'),
    path('<uuid:uuid>/document/<str:username>/', viewsets.PersonAddDocumentView.as_view(), name='add_legacy_document_json'),
    path('<uuid:uuid>/tattoo/<str:username>/', viewsets.PersonAddTattooView.as_view(), name='add_legacy_tattoo_json'),
    path('<uuid:uuid>/nickname/<str:username>/', viewsets.PersonAddNicknameView.as_view(), name='add_legacy_nickname_json'),
    path('<uuid:uuid>/physical/<str:username>/', viewsets.PersonAddPhysicalView.as_view(), name='add_legacy_physical_json')
]
