from django.urls import include, path
from global_login_required import login_not_required

from . import viewsets

app_name = 'apps.person.legacy'

urlpatterns = [
    path('<str:username>/', viewsets.AddPersonView.as_view(), name='add_legacy_person_json'),
    path('<uuid:uuid>/face/<str:username>/', viewsets.PersonAddFaceView.as_view(), name='add_legacy_face_json')
]
