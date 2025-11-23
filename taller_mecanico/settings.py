"""Django settings para el proyecto Taller Mecánico (MySQL)."""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w&tp3y(k4x=7ftr(l@&o8ip@vr^db@=y3zk34$ha)4ewcaesy#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#urls para login y logout
LOGIN_REDIRECT_URL = "/home/"  # o tu vista principal
LOGOUT_REDIRECT_URL = "/login/"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clientes',
    'vehiculo',
    'cotizaciones',
    'servicios',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'taller_mecanico.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cotizaciones.context_processors.empresa_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'taller_mecanico.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taller_mecanico',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True
USE_L10N = False # establecido a False para usar DATE_FORMAT personalizado entonces se podra usar el formato de fecha chileno

USE_TZ = True

# Formato de fecha chileno: día-mes-año (ej: 31-12-2025)
# DATE_FORMAT es usado por el filtro |date en plantillas cuando no se usa localización.
DATE_FORMAT = 'd-m-Y'
# Formatos que acepta Django al parsear fechas en formularios (dd-mm-YYYY)
DATE_INPUT_FORMATS = ['%d-%m-%Y', '%d-%m-%y']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email configuration
# Configuración para envío de emails reales con Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tallermecanicoteam06@gmail.com'
EMAIL_HOST_PASSWORD = 'bjus fxdm cjtt iukq'
DEFAULT_FROM_EMAIL = 'tallermecanicoteam06@gmail.com'

# Para desarrollo/pruebas en consola, comentar lo de arriba y descomentar:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Datos de empresa para autorellenar cotizaciones
EMPRESA_NOMBRE = "Juan Pablo S.A."
EMPRESA_RUT = "21.702.986-4"
EMPRESA_GIRO = "Servicios de Mecánica Automotriz"
EMPRESA_DIRECCION = "Calle Principal 123, Comuna, Ciudad"
EMPRESA_TELEFONO = "+56 9 1234 5678"
EMPRESA_EMAIL = "contacto@tuempresa.cl"