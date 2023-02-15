from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from oauth2.views import exchange_token, expire_token
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
   permission_classes=[permissions.DjangoModelPermissions],
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/auth/validate/<str:backend>/', exchange_token),
    path('api/v1/auth/logout/', expire_token),
    path('', include('auth_oidc.urls'), name='auth_oidc'),
    path('', include('base.urls'), name='base'),
    path('api/v1/alert/', include('apps.alert.api.v1.urls'), name='alert'),
    path('api/v1/bnmp/', include('apps.bnmp.api.v1.urls'), name='bnmp'),
    path('api/v1/cortex/', include('apps.cortex.api.v1.urls'), name='cortex'),
    path('api/v1/document/', include('apps.document.api.urls'), name='document'),
    path('api/v1/person/', include('apps.person.api.v1.urls'), name='person'),
    path('api/v1/vehicle/', include('apps.vehicle.api.v1.urls'), name='vehicle'),
    path('api/v1/image/', include('apps.image.api.urls'), name='image'),
    path('api/v1/address/', include('apps.address.api.urls'), name='address'),
    path('api/v1/legacy/', include('apps.person.api.legacy.urls'), name='legacy'),
    path('api/v1/watermark/', include('apps.watermark.urls'), name='watermark'),
    path('celery-progress/', include('celery_progress.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# swagger
urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa E501
]