from .base import *

# def get_env_variable(env_key, default=None):
#     try:
#         env_value = os.environ[env_key]
#         if env_value in ('True', 'False'):
#             return env_value == 'True'
#         else:
#             return env_value
#     except KeyError:
#         if default is None:
#             error_msg = f'Environment variable "{env_key}" does not configured.'
#             raise ImproperlyConfigured(error_msg)
#         return default

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'NAME': 'test_db',
        'USER': 'root',
        'PASSWORD': 'navi',
        'TEST': {
            'NAME': 'test_db',
        },
    },
}