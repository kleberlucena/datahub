from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from oauth2.views import exchange_token, expire_token
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/validate/<str:backend>/', exchange_token),
    path('auth/logout/', expire_token),
    path('', include('auth_oidc.urls'), name='auth_oidc'),
    path('', include('base.urls'), name='base'),
    path('api/v1/document/', include('apps.document.api.urls'), name='person'),
    path('api/v1/person/', include('apps.person.api.urls'), name='person'),
    path('api/v1/image/', include('apps.image.api.urls'), name='image'),
    path('api/v1/address/', include('apps.address.api.urls'), name='address'),
    path('celery-progress/', include('celery_progress.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# swagger
urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa E501
]