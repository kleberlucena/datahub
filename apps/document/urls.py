from django.urls import include, path
from rest_framework import routers

# from apps.document.views import DocumentView
from apps.document.api.viewset import DocumentViewSet, ImageViewSet

app_name = 'document'

router = routers.DefaultRouter()

router.register(r'', DocumentViewSet)
# router.register(r'images', ImageViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]