DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "fiveScontrol",
        "USER": "admin",
        "PASSWORD": "just4Taqtile",
        "HOST": "localhost",
        "PORT": "5432",
    },
    "test": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
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
