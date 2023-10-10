from django.urls import path

from . import views

app_name = 'person'

urlpatterns = [
    path('api-v1/person_list_json/', views.PersonListJson.as_view(), name='person_list_json'),
    path('list_person/', views.PersonListView.as_view(), name='list_person'),
    path('task-tattoo-api-person/', views.TaskSetEntityFromTattooView.as_view(), name='task-tattoo-api-person'),
    path('task-nickname-api-person/', views.TaskSetEntityFromNicknameView.as_view(), name='task-nickname-api-person'),
    path('task-face-api-person/', views.TaskSetEntityFromFaceView.as_view(), name='task-face-api-person'),
    path('task-physical-api-person/', views.TaskSetEntityFromPhysicalView.as_view(), name='task-physical-api-person'),
    path('task-person-api-person/', views.TaskSetEntityFromPersonView.as_view(), name='task-person-api-person'),
    path('command_person/', views.ComandosAPIPersonView.as_view(), name='command_person'),
    path('search-person/', views.SearchPersonView.as_view(), name='search_person'),
    path('persons/', views.PersonListView.as_view(), name='person-list'),
    path('persons/create/', views.PersonCreateView.as_view(), name='person-create'),
    path('persons/<int:pk>/update/', views.PersonUpdateView.as_view(), name='person-update'),
    path('persons/<int:pk>/delete/', views.PersonDeleteView.as_view(), name='person-delete'),



]
