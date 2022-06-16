from datetime import timedelta
from pathlib import Path
from typing import List, Tuple
import environ


# Environment variable definitions
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

# Variable default of Django
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG', default=False)
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = list(
    filter(lambda h: h != '', env('ALLOWED_HOSTS', default='*').split(','))
)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'auth_oidc',  # O APP auth must come before allauth to load templates

    # Necessary to allauth
    'django.contrib.sites',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.keycloak',

    # Libraries
    'rest_framework',
    'django_minio_backend.apps.DjangoMinioBackendConfig',
    'stdimage',
    'crispy_forms',
    'widget_tweaks',
    'localflavor',
    'django_celery_results',
    'django_celery_beat',
    'celery_progress',

    # Apps
    'base',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_graylog.GraylogMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'global_login_required.GlobalLoginRequiredMiddleware',
]

ROOT_URLCONF = 'project.urls'

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [BASE_DIR / 'base/static/']  # Static on path not default
STATICFILES_STORAGE = 'django_minio_backend.models.MinioBackendStatic'
DEFAULT_FILE_STORAGE = 'django_minio_backend.models.MinioBackend'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

# Allauth
SITE_ID = 2  # int(env('DJANGO_SITE_ID'))  # Verify the site id in django admin"

ACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
ACCOUNT_LOGOUT_REDIRECT_URL = env('KEYCLOAK_ACCOUNT_LOGOUT_REDIRECT_URL')
LOGIN_REDIRECT_URL = '/'
KEYCLOAK_URL = env('KEYCLOAK_URL')
KEYCLOAK_REALM = env('KEYCLOAK_REALM')
OIDC_OP_LOGOUT_ENDPOINT = KEYCLOAK_URL + '/realms/' + KEYCLOAK_REALM + "/protocol/openid-connect/logout"
OIDC_OP_LOGOUT_URL_METHOD = "auth.views.logout"

SOCIALACCOUNT_PROVIDERS = {
    'keycloak': {
        'KEYCLOAK_URL': env('KEYCLOAK_URL'),
        'KEYCLOAK_REALM': env('KEYCLOAK_REALM')
    }
}


# Minio
MINIO_CONSISTENCY_CHECK_ON_START = True
MINIO_ENDPOINT = env('MINIO_ENDPOINT')
MINIO_EXTERNAL_ENDPOINT = env('MINIO_EXTERNAL_ENDPOINT')
MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = True
MINIO_ACCESS_KEY = env('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = env('MINIO_SECRET_KEY')
MINIO_USE_HTTPS = True
MINIO_PRIVATE_BUCKETS = ['bacinf-private']
MINIO_PUBLIC_BUCKETS = ['bacinf-public']
MINIO_MEDIA_FILES_BUCKET = 'bacinf-media'
MINIO_STATIC_FILES_BUCKET = 'bacinf-static'
MINIO_PRIVATE_BUCKETS.append(MINIO_MEDIA_FILES_BUCKET)
MINIO_PUBLIC_BUCKETS.append(MINIO_STATIC_FILES_BUCKET)
MINIO_URL_EXPIRY_HOURS = timedelta(days=1)
MINIO_POLICY_HOOKS: List[Tuple[str, dict]] = []
MINIO_BUCKET_CHECK_ON_SAVE = True

# Global login required middleware
PUBLIC_VIEWS = [
    'auth_oidc.views.logout'
]
PUBLIC_PATHS = [
    r'^/accounts/.*',  # allow public access to all django-allauth views
    r'^/health_check',
]

if DEBUG:
    PUBLIC_PATHS.append(r'^/admin/.*', )  # allow access to admin views
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
    AUTHENTICATION_BACKENDS.append('django.contrib.auth.backends.ModelBackend')
    MINIO_CONSISTENCY_CHECK_ON_START = False
    MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = False
    MINIO_USE_HTTPS = False


# Celery Configuration Options
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 3 * 60 * 60
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

# Graylog
GRAYLOG_ENDPOINT = env('GRAYLOG_HTTP_ENDPOINT')


