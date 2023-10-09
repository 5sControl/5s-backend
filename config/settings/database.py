from config.settings.base import config, BASE_DIR

import sys


DATABASES = {
    "default": {
        "ENGINE": config("DJANGO_DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DJANGO_DB_NAME", default=BASE_DIR / "db.sqlite3"),
        "USER": config("DJANGO_DB_USER", default=None),
        "PASSWORD": config("DJANGO_DB_PASSWORD", default=None),
        "HOST": config("DJANGO_DB_HOST", default=None),
        "PORT": config("DJANGO_DB_PORT", default=None),
    },

    "database_for_test": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_database",
        "USER": "admin",
        "PASSWORD": "just4Taqtile",
        "HOST": "192.168.1.110",
        "PORT": "5433",
    },
}

if "test" in sys.argv:
    DATABASES["default"] = DATABASES["database_for_test"]

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
