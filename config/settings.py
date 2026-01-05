import os
from datetime import timedelta
from pathlib import Path

from environs import env
from kombu import Queue

env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('key')

DEBUG = env('debug')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # internal
    'home.apps.HomeConfig',
    'product.apps.ProductConfig',
    'user.apps.UserConfig',
    'admin_panel.apps.AdminPanelConfig',
    'request.apps.RequestConfig',
    'log.apps.LogConfig',
    # external
    'rest_framework',
    'easyaudit',
    'rest_framework_simplejwt',
    'taggit',
    'corsheaders',
    'django_celery_results',
    'drf_yasg',
    'persiantools',
    'webpush',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': env('template_backend'),
        'DIRS': [ BASE_DIR / "templates" ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = env('wsgi_application')

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

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

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],

    'DEFAULT_THROTTLE_RATES': {'anon': '50/d', 'user': '100/d', 'daily_post': '5/day', 'ten_per_minute': '10/min'},
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'user.authentications.CsrfExemptSessionAuthentication',
    ),
}

AUTH_USER_MODEL = 'user.User'

# CORS_ORIGIN_WHITELIST = (
#     'https://seti4115.pythonanywhere.com',
#     'http://localhost:5173',
#     )

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = 'None'

SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
    "https://seti4115.pythonanywhere.com"
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5173",
    "https://seti4115.pythonanywhere.com"
]
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

CELERY_TIMEZONE = "Asia/Tehran"
CELERY_ENABLE_UTC = False

CELERY_TASK_QUEUES = (
    Queue("db_heavy"),
    Queue("cache_fast"),
)

CELERY_TASK_ROUTES = {
    "apps.requests.tasks_db.*": {"queue": "db_heavy"},
    "apps.requests.tasks_cache.*": {"queue": "cache_fast"},
}

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BIsMeWIG5RoGCyqIH-ThyVn6NGlicZqiB0fmcuhqPOzBZWWu5OCjYCVX6qqiEAuhZFUDwDszRjvj9jX-HmkvH-M",
    "VAPID_PRIVATE_KEY":"0skZydInrX30tgkbV_h14Y_20hNGWSQM0P1AGOPhjlc",
    "VAPID_ADMIN_EMAIL": "1919setareh1919@gmail.com"
}
# {
# "subject": "mailto: <1919setareh1919@gmail.com>",
# "publicKey": "BIsMeWIG5RoGCyqIH-ThyVn6NGlicZqiB0fmcuhqPOzBZWWu5OCjYCVX6qqiEAuhZFUDwDszRjvj9jX-HmkvH-M",
# "privateKey": "0skZydInrX30tgkbV_h14Y_20hNGWSQM0P1AGOPhjlc"
# }

CELERY_BEAT_SCHEDULE = {
    "every_thirty_days": {
        "task": "tasks.db_tasks.cleanup_old_request_logs",
        "schedule": timedelta(days=1),
        "kwargs": {
            "days": 1,
        }
    },
}