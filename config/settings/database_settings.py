from celery.schedules import crontab

from src.Core.const import SERVER_URL


# from .base_settings import BASE_DIR
#
#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "database" / "db.sqlite3",
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fiveScontrol',
        'USER': 'admin',
        'PASSWORD': 'just4Taqtile',
        'HOST': SERVER_URL,
        'PORT': '5432',
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 450,
    }
}


# celery settings
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'send_low_stock_notification': {
        'task': 'mailer.tasks.send_low_stock_notification',
        'schedule': crontab(hour=9, minute=0),
    },
}
