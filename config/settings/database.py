from config.settings.base import config, BASE_DIR

import sys


DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME", default=BASE_DIR / "db.sqlite3"),
        "USER": config("DB_USER", default=None),
        "PASSWORD": config("DB_PASSWORD", default=None),
        "HOST": config("DB_HOST", default=None),
        "PORT": config("DB_PORT", default=None),
    },

    "database_for_test": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("TEST_DB_NAME"),
        "USER": config("DB_USER", default=None),
        "PASSWORD": config("DB_PASSWORD", default=None),
        "HOST": config("DB_HOST", default=None),
        "PORT": config("TEST_DB_PORT", default=None),
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
