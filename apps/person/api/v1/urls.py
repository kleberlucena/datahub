from django.urls import path

from apps.person.api.v1 import viewsets

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
    path('face/<uuid:uuid>/', viewsets.FaceUpdateDestroyView.as_view(), name='update_face_json'),
    path('tattoo/<uuid:uuid>/', viewsets.TattooUpdateDestroyView.as_view(), name='update_tattoo_json'),
    path('nickname/<uuid:uuid>/', viewsets.NicknameUpdateDestroyView.as_view(), name='update_nickname_json'),
    path('physical/<uuid:uuid>/', viewsets.PhysicalUpdateDestroyView.as_view(), name='update_physical_json'),
    path('document/<uuid:uuid>/', viewsets.DocumentUpdateDestroyView.as_view(), name='update_document_json'),
    path('address/<uuid:uuid>/', viewsets.AddressUpdateDestroyView.as_view(), name='update_address_json'),
    path('image/<uuid:uuid>/', viewsets.ImageUpdateDestroyView.as_view(), name='update_destroy_image_json'),
]
