from celery.schedules import crontab
from config.settings.base import config
CELERY_BROKER_URL = "redis://" + config("REDIS_HOST", default="127.0.0.1") + ":6379/1"
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_TIMEZONE = None
CELERY_BEAT_SCHEDULE = {
    "send_low_stock_notification": {
        "task": "src.Mailer.tasks.send_low_stock_notification",
        "schedule": crontab(hour=6, minute=0),
    },
}
