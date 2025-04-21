import json
from .base_settings import *

with open(".env/prod.json", encoding='utf-8') as file:
    env_data = json.load(file)

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