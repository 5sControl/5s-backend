from celery.schedules import crontab

CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_TIMEZONE = None
CELERY_BEAT_SCHEDULE = {
    "send_low_stock_notification": {
        "task": "src.Mailer.tasks.send_low_stock_notification",
        "schedule": crontab(hour=12, minute=30),
    },
}
