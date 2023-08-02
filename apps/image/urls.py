from django.urls import path
from global_login_required import login_not_required

from .views import *

app_name = 'image'

urlpatterns = [
    path('api-v1/image_list_json/', ImageListJson.as_view(), name='image_list_json'),
    path('list_image/', ImageListView.as_view(), name='list_image'),
    path('task-image-api-entity/', TaskSetEntityFromImageView.as_view(), name='task-image-api-entity'),
    path('command_image/', CommandsAPIImageView.as_view(), name='command_image'),
]
