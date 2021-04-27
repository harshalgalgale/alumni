#!/usr/bin/python
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR,  ".env")

# If a local .env doesn't exist, create one by loading it from Secret Manager.
if not os.path.isfile(env_file):
    import google.auth
    from google.cloud import secretmanager_v1 as sm

    _, project = google.auth.default()

    if project:
        client = sm.SecretManagerServiceClient()
        settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
        name = f"projects/{project}/secrets/{settings_name}/versions/latest"
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

        with open(env_file, "w") as f:
            f.write(payload)

env = environ.Env()
env.read_env(env_file)

root = environ.Path(__file__) - 3
SITE_ROOT = root()

DEBUG = env("DEBUG", default=False)

SECRET_KEY = env("SECRET_KEY")

if "CURRENT_HOST" in os.environ:
    # handle raw host(s), or http(s):// host(s), or no host. 
    HOSTS = []
    for h in env.list("CURRENT_HOST"):
        if "://" in h:
            h = h.split("://")[1]
        HOSTS.append(h)
else:
    # Assume localhost if no CURRENT_HOST
    HOSTS = ["localhost"]

ALLOWED_HOSTS = ["127.0.0.1"] + HOSTS

# Enable Django security precautions if *not* running locally
if "localhost" not in ALLOWED_HOSTS:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party Apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'import_export',
    'drf_yasg',
    # 'country_regions',

    # Application definition
    "unicodex",
    'accounts',
    'students',
    'core',
    'committee',
    'members',
    'article',
    'career',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATIC_ROOT = "/static/"
GS_BUCKET_NAME = env("GS_BUCKET_NAME", default=None)

if GS_BUCKET_NAME: 
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"

    INSTALLED_APPS += ["storages"]

else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    STATIC_URL = STATIC_ROOT

    MEDIA_ROOT = "media/"  # where files are stored on the local filesystem
    MEDIA_URL = "/media/"  # what is prepended to the image URL


ROOT_URLCONF = "unicodex.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "unicodex.wsgi.application"

WEB_ENV =  env("WEB_ENV", default='prod')
if WEB_ENV != 'local':
    DATABASES = {"default": env.db()}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR,  "db.sqlite3"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    "http://localhost:4200",
    'https://alumni-dev-13042021.nw.r.appspot.com'
]

WEB_ENV = env("WEB_ENV", default='prod')

if WEB_ENV == 'local':
    EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SENDGRID_API_KEY = env('SENDGRID_API_KEY', default='')

EMAIL_HOST = env('SENDGRID_API_KEY', default='smtp.sendgrid.net')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER = 'noreply@alumni.com'
DEFAULT_REPLY_TO_EMAIL = 'hello@alumni.com'

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,  # add Django Login and Django Logout buttons, CSRF token to swagger UI page
    # 'LOGIN_URL': getattr(django.conf.settings, 'LOGIN_URL', None),  # URL for the login button
    # 'LOGOUT_URL': getattr(django.conf.settings, 'LOGOUT_URL', None),  # URL for the logout button

    # Swagger security definitions to include in the schema;
    # see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object
    'SECURITY_DEFINITIONS': {
        # 'basic': {
        #     'type': 'basic'
        # },
        'JWTAuthentication': {
            'description': 'Uses Bearer Authentication (also called token authentication). You must include an Authorization header when making requests to the API',
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
    },

    # url to an external Swagger validation service; defaults to 'http://online.swagger.io/validator/'
    # set to None to disable the schema validation badge in the UI
    'VALIDATOR_URL': '',

    # swagger-ui configuration settings, see https://github.com/swagger-api/swagger-ui/blob/112bca906553a937ac67adc2e500bdeed96d067b/docs/usage/configuration.md#parameters
    'OPERATIONS_SORTER': None,
    'TAGS_SORTER': None,
    'DOC_EXPANSION': 'list',
    'DEEP_LINKING': False,
    'SHOW_EXTENSIONS': True,
    'DEFAULT_MODEL_RENDERING': 'model',
    'DEFAULT_MODEL_DEPTH': 2,
}

REDOC_SETTINGS = {
    # ReDoc UI configuration settings, see https://github.com/Rebilly/ReDoc#redoc-tag-attributes
    'LAZY_RENDERING': True,
    'HIDE_HOSTNAME': False,
    'EXPAND_RESPONSES': 'all',
    'PATH_IN_MIDDLE': False,
}
