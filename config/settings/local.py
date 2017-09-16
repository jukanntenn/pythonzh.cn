from .common import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', default='si^7v_103dy=alrw5q9sif^7c&m25=9g#s^)e*!xngzoxew92j')

DEBUG = True
