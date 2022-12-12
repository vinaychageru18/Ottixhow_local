from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ottixhowdb',
        'ENFORCE_SCHEMA': False,
    }
}

DEFAULT_ADMIN = 'admin'


servers =  None
username = None
password = None

CACHES = None