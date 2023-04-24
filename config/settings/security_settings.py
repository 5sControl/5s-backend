AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
    "http://localhost:5500",
    "http://localhost:3000",
    "https://localhost:8000",
    "https://*.eu.ngrok.io",
    "http://*.eu.ngrok.io",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
    "http://192.168.1.101:8000",
    "http://192.168.1.101:3000",
    "http://0.0.0.0:8000",
    "http://*",
    "https://*",
    "https://cfce-81-7-77-205.ngrok-free.app/",
]

CSRF_TRUSTED_ORIGINS = [
    "http://*",
    "https://*",
    "https://fe9e-134-17-26-206.eu.ngrok.io/",
    "https://cfce-81-7-77-205.ngrok-free.app/"
]
