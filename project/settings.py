import errno
import os
import environ
from pathlib import Path
from datetime import timedelta
from typing import List, Tuple

# Environment variable definitions
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

# Variable default of Django
SECRET_KEY = env('SECRET_KEY')
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

    # Apps
    'base',
    'names',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'global_login_required.GlobalLoginRequiredMiddleware',
]

ROOT_URLCONF = 'project.urls'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
STATICFILES_DIRS = [BASE_DIR / 'base/static/']  # Static on path not default
STATICFILES_STORAGE = 'django_minio_backend.models.MinioBackendStatic'
DEFAULT_FILE_STORAGE = 'django_minio_backend.models.MinioBackend'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

# Allauth
SITE_ID = int(env('SITE_ID'))  # Verify the site id in django admin"

ACCOUNT_LOGOUT_REDIRECT_URL = env('ACCOUNT_LOGOUT_REDIRECT_URL')
LOGIN_REDIRECT_URL = '/'
KEYCLOAK_URL = env('KEYCLOAK_URL')
KEYCLOAK_REALM = env('KEYCLOAK_REALM')
OIDC_OP_LOGOUT_ENDPOINT = KEYCLOAK_URL + "/realms/" + KEYCLOAK_REALM + "/protocol/openid-connect/logout"
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
MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = False
MINIO_ACCESS_KEY = env('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = env('MINIO_SECRET_KEY')
MINIO_USE_HTTPS = False
MINIO_PRIVATE_BUCKETS = [env('MINIO_PRIVATE_BUCKETS')]
MINIO_PUBLIC_BUCKETS = [env('MINIO_PUBLIC_BUCKETS')]
MINIO_URL_EXPIRY_HOURS = timedelta(days=1)
MINIO_POLICY_HOOKS: List[Tuple[str, dict]] = [
    # ('django-backend-dev-private', dummy_policy)
]
MINIO_MEDIA_FILES_BUCKET = env('MINIO_MEDIA_FILES_BUCKET')
MINIO_STATIC_FILES_BUCKET = env('MINIO_STATIC_FILES_BUCKET')
MINIO_BUCKET_CHECK_ON_SAVE = True

# Global login required middleware
PUBLIC_VIEWS = [
    'base.views.health_check',  # view to verify health system status
    'auth_oidc.views.logout'
]
PUBLIC_PATHS = [
    r'^/accounts/.*',  # allow public access to all django-allauth views
]

if DEBUG:
    PUBLIC_PATHS.append(r'^/admin/.*', )  # allow access to admin views


# Logs
PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
LOG_FILE_PATH = '{}/logs/app.log'.format(PROJECT_ROOT)

if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
    try:
        os.makedirs(os.path.dirname(LOG_FILE_PATH))
    except OSError as ex:  # Guard against race condition
        if ex.errno != errno.EEXIST:
            raise

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },

    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 15,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        # string empty will capture all module logs
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        },
    },
}
