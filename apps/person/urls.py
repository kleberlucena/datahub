from django.urls import include, path
from global_login_required import login_not_required

from .views import *
from .api import viewsets

app_name = 'apps.person'

urlpatterns = [
    path('', login_not_required(viewsets.AddPersonView.as_view()), name='add_person_json'),
    path('<uuid:uuid>/', login_not_required(viewsets.PersonRetrieve.as_view()), name='retrieve_json'),
    path('<uuid:uuid>/face/', login_not_required(viewsets.PersonAddFaceView.as_view()), name='add_face_json'),
    path('<uuid:uuid>/tatoo/', login_not_required(viewsets.PersonAddTatooView.as_view()), name='add_tatoo_json'),
    path('<uuid:uuid>/nickname/', login_not_required(viewsets.PersonAddNicknameView.as_view()), name='add_nickname_json'),
    path('<uuid:uuid>/physical/', login_not_required(viewsets.PersonAddPhysicalView.as_view()), name='add_physical_json'),
    path('<uuid:uuid>/document/', login_not_required(viewsets.PersonAddDocumentView.as_view()), name='add_document_json'),
    path('<uuid:uuid>/address/', login_not_required(viewsets.PersonAddAddressView.as_view()), name='add_address_json'),
    path('<uuid:uuid>/image/', login_not_required(viewsets.PersonAddImageView.as_view()), name='add_image_json'),
    path('face/<uuid:uuid>/', login_not_required(viewsets.FaceUpdateView.as_view()), name='update_face_json'),
    path('tatoo/<uuid:uuid>/', login_not_required(viewsets.TatooUpdateView.as_view()), name='update_tatoo_json'),
    path('nickname/<uuid:uuid>/', login_not_required(viewsets.NicknameUpdateView.as_view()), name='update_nickname_json'),
    path('physical/<uuid:uuid>/', login_not_required(viewsets.PhysicalUpdateView.as_view()), name='update_physical_json'),
    path('document/<uuid:uuid>/', login_not_required(viewsets.DocumentUpdateView.as_view()), name='update_document_json'),
    path('address/<uuid:uuid>/', login_not_required(viewsets.AddressUpdateView.as_view()), name='update_address_json'),
]
