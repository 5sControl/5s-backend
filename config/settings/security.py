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

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'ngrok-skip-browser-warning',
]


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
    "https://d84d-81-7-77-205.ngrok-free.app",
    "https://grand-alien-apparently.ngrok-free.app",
    "https://5scontrol.serveo.net"
]

CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8000",
    "https://*.eu.ngrok.io",
    "https://d84d-81-7-77-205.ngrok-free.app",
    "https://grand-alien-apparently.ngrok-free.app",
    "https://5scontrol.serveo.net",
]
