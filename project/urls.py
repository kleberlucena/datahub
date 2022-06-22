from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('auth_oidc.urls'), name='auth_oidc'),
    path('', include('base.urls'), name='base'),
    path('celery-progress/', include('celery_progress.urls')),
    path('person/', include('apps.person.urls'), name='person'),
    path('image/', include('apps.image.urls'), name='image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
