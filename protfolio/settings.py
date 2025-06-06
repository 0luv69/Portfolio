import os
from pathlib import Path
import dj_database_url


from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# security settings   
SECRET_KEY = str(os.getenv('SECRET_KEY'))
DEBUG = str(os.getenv('DEBUG')).lower() == 'true'
PRODUCTION_ENV = str(os.getenv('PRODUCTION_ENV')).lower() == 'true'
USE_SQLITE = str(os.getenv('USE_SQLITE')).lower() == 'true'



ALLOWED_HOSTS = ["127.0.0.1", 'localhost']
if PRODUCTION_ENV:
    ALLOWED_HOSTS += ['.vercel.app', "www.rujalbaniya.com.np", "rujalbaniya.com.np"]



# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',

    "tailwind",
    'theme',
    'whitenoise.runserver_nostatic',
]

# tailwind configutation 
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'protfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'protfolio.wsgi.application'


# Database
if USE_SQLITE:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

elif PRODUCTION_ENV:
    DATABASES = {
        'default': dj_database_url.parse(
        os.getenv('DATABASE_URL'),
        conn_max_age=600,    # persistent connections
        ssl_require=True     # Neon requires SSL
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': str(os.getenv('PROD_NAME')),
            'USER': 'postgres',
            'PASSWORD': str(os.getenv('PROD_PASSWORD')),
            'HOST': str(os.getenv('PROD_HOST')),
            'PORT': str(os.getenv('PROD_PORT')),
        }
    }
    

     





# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = '/static/'

if PRODUCTION_ENV:
    STATIC_URL = '/staticfiles/'
STATICFILES_DIRS= [os.path.join(BASE_DIR, 'public/static/'), os.path.join(BASE_DIR, 'theme', 'static', 'css', 'dist'),]

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/static/')



STATIC_ROOT= os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# goolge email settings
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = str(os.getenv('EMAIL_USE_TLS')).lower() == 'true'
EMAIL_USE_SSL = str(os.getenv('EMAIL_USE_SSL')).lower() == 'true'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
