import json
from .base_settings import *
import os

LOG_DIR = "/logs/indie"

os.makedirs(LOG_DIR, exist_ok=True)

with open(".env/prod.json", encoding='utf-8') as file:
    env_data = json.load(file)

SECRET_KEY = f'django-insecure-{env_data["django_secret_key"]}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env_data["db_schema"],
        'USER': env_data["db_user"],
        'PASSWORD': env_data["db_password"],
        'HOST': env_data["db_host"],
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(levelname)s] %(asctime)s %(name)s.%(funcName)s:%(lineno)s %(message)s",
            "datefmt": "%Y-%m-%d %H;%M",
        },
        "verbose": {
            "format": "[%(levelname)s] %(asctime)s %(name)s.%(funcName)s:%(lineno)s %(message)s",
            "datefmt": "%Y-%m-%d %H;%M",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "/logs/indie/error.log",
            "when": "midnight", # 자정에 파일 갱신
            "backupCount": 7, # 7일간 유효
            "formatter": "verbose",
        },
        "django": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "/logs/indie/django.log",
            "when": "midnight", # 자정에 파일 갱신
            "backupCount": 7, # 7일간 유효
            "formatter": "verbose",
        },
    },
    "loggers": {
        "error": {
            "handlers": ["error", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django": {
            "handlers": ["django", "console"],
            "level": "INFO",
            "propagate": False,
        },
    }
}

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True