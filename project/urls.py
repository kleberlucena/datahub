from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from oauth2.views import exchange_token, expire_token
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "person",
                "description": "everything about People API"
            },
            {
                "name": "bnmp",
                "description": "everything about People BNMP CORTEX API"
            },
            {
                "name": "vehicle",
                "description": "everything about Vehicle API and Vehicle CORTEX API"
            },
            {
                "name": "cortex",
                "description": "everything about People CORTEX API"
            },
            {
                "name": "alert",
                "description": "everything about People and Vehicle alerts CORTEX API"
            },
        ]

        return swagger


schema_view = get_schema_view(
    openapi.Info(
        title="Bacinf API",
        default_version='V1',
        description="Base Central de Informações",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    generator_class=CustomOpenAPISchemaGenerator,
    permission_classes=[permissions.DjangoModelPermissions],
    public=True,
)


urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/auth/validate/<str:backend>/', exchange_token),
    path('api/v1/auth/logout/', expire_token),
    path('', include('auth.auth_oidc.urls'), name='auth_oidc'),
    path('', include('base.urls'), name='base'),
    path('api/v1/alert/', include('apps.alert.api.v1.urls'), name='alert'),
    path('api/v1/bnmp/', include('apps.bnmp.api.v1.urls'), name='bnmp'),
    path('api/v1/cortex/', include('apps.cortex.api.v1.urls'), name='cortex'),
    path('api/v1/document/', include('apps.document.api.urls'), name='document_api'),
    path('api/v1/fact/', include('apps.fact.api.v1.urls'), name='fact'),
    path('api/v1/police-report/',
         include('apps.police_report.api.v1.urls'), name='police_report'),
    path('api/v1/person/', include('apps.person.api.v1.urls'), name='person_api'),
    path('api/v1/vehicle/', include('apps.vehicle.api.v1.urls'), name='vehicle_api'),
    path('api/v1/image/', include('apps.image.api.urls'), name='image_api'),
    path('api/v1/address/', include('apps.address.api.urls'), name='address_api'),
    path('api/v1/base/', include('base.api.v1.urls'), name='base_api'),
    path('api/v1/legacy/', include('apps.person.api.legacy.urls'), name='legacy_api'),
    path('api/v1/watermark/', include('apps.watermark.urls'), name='watermark'),
    path('api/v1/radio/', include('apps.radio.api.v1.urls'), name='radio_api'),
    path('address/', include('apps.address.urls'), name='address'),
    path('document/', include('apps.document.urls'), name='document'),
    path('image/', include('apps.image.urls'), name='image'),
    path('person/', include('apps.person.urls'), name='person'),
    path('portal/', include('apps.portal.urls'), name='portal'),
    path('protect_network/', include('apps.protect_network.urls'), name='protect_network'),
    path('termos-de-uso/', include('apps.termsofuse.urls')),
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
