from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'admin_user',
        'PASSWORD': '13131313',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
