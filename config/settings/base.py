from pathlib import Path

import os

from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY", default="default_secret_key")

LICENSE_ACTIVE = config("LICENSE_ACTIVE", default=False, cast=bool)

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # Third party application
    "django_filters",
    "rest_framework",
    "djoser",
    "corsheaders",
    "drf_yasg",
    "django_redis",
    "django_celery_results",
    "django_celery_beat",
    "django_extensions",
    "django_crontab",
    # Common application
    "src.newOrderView",
    "src.CameraAlgorithms",
    "src.OrderView",
    "src.DatabaseConnections",
    "src.CompanyLicense.apps.CompanyLicenseConfig",
    "src.Healthcheck.apps.HealthcheckConfig",
    "src.Inventory.apps.InventoryConfig",
    "src.Employees.apps.EmployeesConfig",
    "src.Suppliers.apps.SuppliersConfig",
    "src.manifest_api.apps.ManifestApiConfig",
    # Collections reports
    "src.Reports.apps.ReportsConfig",
    "src.ImageReport.apps.ImageConfig",
    "src.Mailer.apps.MailerConfig",
    "src.Core.apps.CoreConfig",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]


ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Etc/GMT"

USE_I18N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
STATIC_URL = "/api/static/"

MEDIA_URL = "/images/"
MEDIA_ROOT = BASE_DIR / "images/"

VIDEO_URL = "/videos/"
VIDEO_ROOT = BASE_DIR / "videos/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
