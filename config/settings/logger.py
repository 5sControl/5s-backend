import logging
from django.utils.log import DEFAULT_LOGGING

# Получение конфигурации логгера по умолчанию
LOGGING = DEFAULT_LOGGING

# Обновление форматирования логов
LOGGING["formatters"]["verbose"] = {
    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
}

# Добавление обработчика "file"
LOGGING["handlers"]["file"] = {
    "class": "logging.FileHandler",
    "filename": "log/logs.log",
    "formatter": "verbose",
}

# Добавление обработчика "console" (если требуется)
LOGGING["handlers"]["console"]["formatter"] = "verbose"

# Применение настроек логгера
logging.config.dictConfig(LOGGING)
