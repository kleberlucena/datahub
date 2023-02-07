from django.urls import path

from . import views

app_name = 'watermark'

urlpatterns = [
    path('<int:pk>/<uuid:uuid>/', views.get_image_url, name='json_image_url'),
]