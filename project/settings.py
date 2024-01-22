from datetime import timedelta
from pathlib import Path
from typing import List, Tuple
import environ
import requests
import json
import os

# Environment variable definitions
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

# Variable default of Django
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG', default=False)
BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}

ALLOWED_HOSTS = list(
    filter(lambda h: h != '', env('ALLOWED_HOSTS', default='*').split(','))
)

# Configurações de CORS.
CORS_URLS_REGEX = r'^/api/v1/.*$'
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "https://portal.stage.pm.pb.gov.br",
        "https://sasp.stage.pm.pb.gov.br",
        "https://sai.stage.pm.pb.gov.br",
        "https://services.stage.pm.pb.gov.br",
        "https://s3.stage.pm.pb.gov.br",
        "https://portal.apps.pm.pb.gov.br",
        "https://sasp.apps.pm.pb.gov.br",
        "https://sai.apps.pm.pb.gov.br",
        "https://services.apps.pm.pb.gov.br",
        "https://s3.apps.pm.pb.gov.br",
    ]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
]


# Application definition

INSTALLED_APPS = [
    'polymorphic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.postgres',

    'auth.auth_oidc',  # O APP auth must come before allauth to load templates
    'oauth2',  # Include authenticate token

    # Necessary to allauth
    'django.contrib.sites',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.keycloak',

    # Libraries
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'rest_framework.authtoken',  # if you use the same token auth system as the example
    'social_django',  # python social auth
    'django_minio_backend.apps.DjangoMinioBackendConfig',
    'stdimage',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'localflavor',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'celery_progress',
    'guardian',
    'leaflet',
    'corsheaders',

    # Apps
    'base',
    'auth.api_oidc_provider',
    'apps.portal',
    'apps.cortex',
    'apps.person',
    'apps.image',
    'apps.address',
    'apps.document',
    'apps.alert',
    'apps.bnmp',
    'apps.vehicle',
    'apps.watermark',
    'apps.fact',
    'apps.police_report',
    'apps.rpa',
    'apps.radio',
    'apps.termsofuse',
    'apps.protect_network',
    'apps.area',
    'apps.georeference',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
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
    'social_core.backends.keycloak.KeycloakOAuth2',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
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
                'base.context_processors.portal_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
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

# Expiration Cookie
SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

# Allauth
SITE_ID = 2  # int(env('DJANGO_SITE_ID'))  # Verify the site id in django admin

ACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_STORE_TOKENS = True  # Necessary to logout
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_LOGOUT_REDIRECT_URL = env('KEYCLOAK_ACCOUNT_LOGOUT_REDIRECT_URL')
LOGIN_REDIRECT_URL = '/'
KEYCLOAK_URL = env('KEYCLOAK_URL')
KEYCLOAK_REALM = env('KEYCLOAK_REALM')
OIDC_OP_LOGOUT_ENDPOINT = KEYCLOAK_URL + '/realms/' + \
    KEYCLOAK_REALM + "/protocol/openid-connect/logout"
OIDC_OP_LOGOUT_URL_METHOD = "auth.views.logout"

SOCIALACCOUNT_PROVIDERS = {
    'keycloak': {
        'KEYCLOAK_URL': env('KEYCLOAK_URL'),
        'KEYCLOAK_REALM': env('KEYCLOAK_REALM')
    }
}

SOCIALACCOUNT_ADAPTER = 'auth.auth_oidc.adapter.PMPBSocialAccountAdapter'

response_sso = requests.get(f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/")
sso_public_key = json.loads(response_sso.text)["public_key"]
KEYCLOAK_SERVER_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----".format(
    sso_public_key)

# Python Social Auth https://github.com/coriolinus/oauth2-article
SOCIAL_AUTH_KEYCLOAK_KEY = env('SOCIAL_AUTH_KEYCLOAK_KEY')
SOCIAL_AUTH_KEYCLOAK_SECRET = env('SOCIAL_AUTH_KEYCLOAK_SECRET')
SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY = sso_public_key
SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL = env(
    'SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL')
SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL = env(
    'SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL')
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_KEYCLOAK_SCOPE = ['email', 'openid']
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    # <- this line not included by default
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Portal
PORTAL_TOKEN = env('PORTAL_TOKEN')
PORTAL_URL_BASE = env('PORTAL_URL_BASE')
PORTAL_RELATIVE_URL_LIST_MILITARY = env('PORTAL_RELATIVE_URL_LIST_MILITARY')
PORTAL_RELATIVE_URL_LIST_ENTITY = env('PORTAL_RELATIVE_URL_LIST_ENTITY')

SELF_URL_BASE = env('SELF_URL_BASE')

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

# Config debug toolbar
INTERNAL_IPS = ["127.0.0.1",]

# Services
SERVICES_URL = env('SERVICES_URL')
SERVICES_ENDPOINT_MARK = env('SERVICES_ENDPOINT_MARK')
SERVICES_TOKEN = env('SERVICES_TOKEN')

# Global login required middleware
PUBLIC_VIEWS = [
    'auth.auth_oidc.views.logout'
]
PUBLIC_PATHS = [
    r'^/accounts/.*',  # allow public access to all django-allauth views
    r'^/health_check',
    r'^/auth/logout/',
    r'^/info_user_inactivate/',
    r'^/api/v1/.*',
    r'^/api/token/refresh/',
    r'^/watermark/.*',
    # Descomentar para expor rota adminitrativa (só para ajustes de configurações do keycloak)
    r'^/admin/.*',
]

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

# Config to run in localhost
if DEBUG:
    PUBLIC_PATHS.append(r'^/admin/.*', )  # allow access to admin views
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
    AUTHENTICATION_BACKENDS.append('django.contrib.auth.backends.ModelBackend')
    MINIO_CONSISTENCY_CHECK_ON_START = False
    MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = False
    MINIO_USE_HTTPS = False
    PROJECT_PORT = env("PROJECT_PORT")
    # INSTALLED_APPS.append('debug_toolbar')  # module to debug
    # MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(
        'rest_framework.authentication.SessionAuthentication')


# REDIS CACHE LOCAL CONFIG
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         # Replace for cloud server IP
#         'LOCATION': 'redis://127.0.0.1:6379/1',  
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }
