from django.urls import path

from . import viewsets

app_name = 'apps.police_report'

urlpatterns = [
    path(
        '', viewsets.PoliceReportViewSet.as_view({'get': 'list', 'post': 'create'}), name='police_report_json'),
    path('<uuid:uuid>/', viewsets.PoliceReportRetrieveViewSet.as_view(),
         name='police_report_retrieve_json'),
    path('<uuid:uuid>/involved-person/', viewsets.PoliceReportAddInvolvedPersonViewSet.as_view(),
         name='police_report_add_involved_person_json'),
    path('characteristics-types/', viewsets.CharacteristicTypeListViewSet.as_view(),
         name='characteristic_type_json'),
    path(
        'vtr/', viewsets.VTRViewSet.as_view({'get': 'list', 'post': 'create'}), name='vtr_json'),
    path('police-team/', viewsets.PoliceTeamViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='police_team_json'),
    path('involved-person/', viewsets.InvolvedPersonViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='involved_person_json'),
    path('involved-person/<uuid:uuid>/', viewsets.InvolvedPersonRetrieveViewSet.as_view(),
         name='involved_person_retrieve_json'),
    path('involved-person/<uuid:uuid>/document/',
         viewsets.InvolvedPersonAddDocumentViewSet.as_view(), name='involved_person_add_document_json'),
    path('involved-person/<uuid:uuid>/personalcharacteristic/',
         viewsets.InvolvedPersonAddPersonalCharacteristicViewSet.as_view(), name='involved_person_add_personalcharacteristic_json'),
    path('involved-person/<uuid:uuid>/address/',
         viewsets.InvolvedPersonAddAddressViewSet.as_view(), name='involved_person_add_address_json'),
    path('involved-person/<uuid:uuid>/image/',
         viewsets.InvolvedPersonAddImageViewSet.as_view(), name='involved_person_add_image_json'),
]
