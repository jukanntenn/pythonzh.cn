from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['.pythonzh.cn']

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
# EMAIL_PORT = os.environ.get('DJANGO_EMAIL_PORT')
# EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')

# EMAIL_USE_SSL = True

# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# django anymail grid
ANYMAIL = {
    "SENDGRID_API_KEY": "XluOweBmpZSGVbD7vivklLpRhYxQ.Rz-rR-a.bJJJT7Bw6RwBb-AUAXEGCvTweWDpvqY",
    # "MAILGUN_SENDER_DOMAIN": 'mg.example.com',
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "Pythonzhcn <noreply@pythonzh.cn>"
