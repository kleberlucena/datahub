from django.urls import include, path
from global_login_required import login_not_required
from rest_framework import routers

# from apps.document.views import DocumentView
from apps.document.api.viewset import DocumentViewSet, DocumentTypeListViewSet

app_name = 'document'

router = routers.DefaultRouter()

router.register(r'', DocumentViewSet)
# router.register(r'images', ImageViewSet)

urlpatterns = [
    path('document-types/', DocumentTypeListViewSet.as_view(), name='document_type_json'),
    path("", include(router.urls)),
]