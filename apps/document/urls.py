from django.urls import path

from .views import *

app_name = 'document'

urlpatterns = [
    path('api-v1/document_list_json/', DocumentListJson.as_view(), name='document_list_json'),
    path('list_document/', DocumentListView.as_view(), name='list_document'),
    path('task-document-api-entity/', TaskSetEntityFromDocumentView.as_view(), name='task-document-api-entity'),
    path('command_document/', CommandsAPIDocumentView.as_view(), name='command_document'),
    path('api-v1/document_image_list_json/', DocumentImageListJson.as_view(), name='document_image_list_json'),
    path('list_document_image/', DocumentImageListView.as_view(), name='list_document_image'),
    path('task-document-image-api-entity/', TaskSetEntityFromDocumentImageView.as_view(), name='task-document-image-api-entity'),
]