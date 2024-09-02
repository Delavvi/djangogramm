from .base import *
from dotenv import load_dotenv
import environ
import os
from google.oauth2 import service_account

DEBUG = True


env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': '5432',
    }
}

SERVICE_ACCOUNT_JSON = os.path.join(BASE_DIR, 'djangogramm/django-418614-c68096b6f432.json')
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_JSON)
MEDIA_URL = os.environ.get('MEDIA_URL')
GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID')
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
GS_CREDENTIALS = credentials
STORAGES = {"staticfiles": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"},
            "default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"}}
BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'polls/static'),
]


