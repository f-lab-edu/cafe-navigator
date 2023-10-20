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
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': get_env_variable('DB_HOST'),
#         'PORT': get_env_variable('DB_PORT'),
#         'NAME': get_env_variable('DB_NAME'),
#         'USER': get_env_variable('DB_USER'),
#         'PASSWORD': get_env_variable('DB_PASSWORD'),
#         'TEST': {
#             'NAME': 'test_db',
#         },
#     },
# }