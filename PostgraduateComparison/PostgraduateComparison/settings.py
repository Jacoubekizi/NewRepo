
from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=w_h_if-@9#_=jr&v)hq%jrx0hzkvcl%hfqite3p-&xyy%7gy('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

# Application definition

INSTALLED_APPS = [
    'application.apps.MyAdminSite',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'application.apps.ApplicationConfig',
    'accounts.apps.AccountsConfig',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'import_export',
    'django_object_actions',
    'imagekit',
    'drf_yasg',
    # 'debug_toolbar'
]


# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://192.168.227.184:6379/",
#         "OPTIONS": {
#             # "CLIENT_CLASS" : "django_redis.client.DefaultClient"
#         }
#     }
# }
AUTH_USER_MODEL = 'accounts.CustomUser'
# ACCOUNT_UNIQUE_EMAIL= True

REST_FRAMEWORK = {

    'NON_FIELD_ERRORS_KEY':'error',


    'DEFAULT_AUTHENTICATION_CLASSES':(
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'PostgraduateComparison.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'PostgraduateComparison.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql',
        'NAME':'Enter your name database',
        'USER':'enter username',
        'PASSWORD':'enter password',
        'HOST':'localhost',
        'PORT':'5432'
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) 
STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'application/static'),
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

}
# setting email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Replace with your preferred backend
EMAIL_HOST = 'smtp.gmail.com' # Replace with your email host for gmail -> 'smtp.gmail.com'
EMAIL_PORT = 587  # Replace with your email port
EMAIL_USE_TLS = True  # Set to False if your email server doesn't use TLS
EMAIL_HOST_USER = 'example@gmail.com'  # Replace with your email username
EMAIL_HOST_PASSWORD = 'password'  # Replace with your email password
