from django.urls import include, path
from global_login_required import login_not_required

from . import viewsets

app_name = 'apps.person'

urlpatterns = [
    path('', viewsets.AddPersonListView.as_view(), name='add_list_person_json'),
    path('<uuid:uuid>/', viewsets.PersonRetrieveDestroyView.as_view(), name='retrieve_json'),
    path('<uuid:uuid>/face/', viewsets.PersonAddFaceView.as_view(), name='add_face_json'),
    path('<uuid:uuid>/tattoo/', viewsets.PersonAddTattooView.as_view(), name='add_tattoo_json'),
    path('<uuid:uuid>/nickname/', viewsets.PersonAddNicknameView.as_view(), name='add_nickname_json'),
    path('<uuid:uuid>/physical/', viewsets.PersonAddPhysicalView.as_view(), name='add_physical_json'),
    path('<uuid:uuid>/document/', viewsets.PersonAddDocumentView.as_view(), name='add_document_json'),
    path('<uuid:uuid>/address/', viewsets.PersonAddAddressView.as_view(), name='add_address_json'),
    path('<uuid:uuid>/image/', viewsets.PersonAddImageView.as_view(), name='add_image_json'),
    path('face/<uuid:uuid>/', viewsets.FaceUpdateView.as_view(), name='update_face_json'),
    path('tattoo/<uuid:uuid>/', viewsets.TattooUpdateView.as_view(), name='update_tattoo_json'),
    path('nickname/<uuid:uuid>/', viewsets.NicknameUpdateView.as_view(), name='update_nickname_json'),
    path('physical/<uuid:uuid>/', viewsets.PhysicalUpdateView.as_view(), name='update_physical_json'),
    path('document/<uuid:uuid>/', viewsets.DocumentUpdateView.as_view(), name='update_document_json'),
    path('address/<uuid:uuid>/', viewsets.AddressUpdateView.as_view(), name='update_address_json'),
]
