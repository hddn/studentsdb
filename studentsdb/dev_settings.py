# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'js*6)f*2jp+u!qtr+25s&80o*pl(bo*b1l7=(4x_%o#x!hpp$i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

PORTAL_URL = 'http://192.168.11.56:8000'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'students_db',
        'USER': 'stdb',
        'PASSWORD': 'students_db',
        'HOST': 'localhost',
        'PORT': '',
        'TEST': {
            'CHARSET': 'utf8',
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMIN_EMAIL = 'admin@gmail.com'

MEDIA_URL = '/media/'
