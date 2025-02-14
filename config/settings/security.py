from decouple import config

existing_cors_whitelist = config("CORS_ORIGIN_WHITELIST", default="").split(',')
existing_csrf_origins = config("CSRF_TRUSTED_ORIGINS", default="").split(',')



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
    'access-control-allow-origin',
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
    "http://localhost:3002",
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
    "https://pleasant-bluejay-next.ngrok-free.app",
    "https://crucial-heron-vastly.ngrok-free.app",
    "https://office.5scontrol.com",
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8000",
    "https://*.eu.ngrok.io",
    "https://d84d-81-7-77-205.ngrok-free.app",
    "https://grand-alien-apparently.ngrok-free.app",
    "https://crucial-heron-vastly.ngrok-free.app",
    "https://pleasant-bluejay-next.ngrok-free.app",
    "https://office.5scontrol.com",
    "http://localhost:5173",
]

CORS_ORIGIN_WHITELIST.extend(existing_cors_whitelist)
CSRF_TRUSTED_ORIGINS.extend(existing_csrf_origins)
