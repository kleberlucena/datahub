from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from oauth2.views import exchange_token


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/<str:backend>/', exchange_token),
    path('', include('auth_oidc.urls'), name='auth_oidc'),
    path('', include('base.urls'), name='base'),
    path('celery-progress/', include('celery_progress.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
