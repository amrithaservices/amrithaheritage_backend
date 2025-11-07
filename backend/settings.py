from pathlib import Path
import os
from decouple import config
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config('SECRET_KEY', default='django-insecure-*w1g8rlopoeb&#@cfo186p!m&-cnq=w4)zs1n=g@gal89e(t&(')


DEBUG = config('DEBUG', default=True, cast=bool)

DEFAULT_ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'amrithaheritage.com',
    'www.amrithaheritage.com',
    '.onrender.com',
]
ENV_ALLOWED_HOSTS = [h.strip() for h in config('ALLOWED_HOSTS', default='').split(',') if h.strip()]
ALLOWED_HOSTS = list(dict.fromkeys(DEFAULT_ALLOWED_HOSTS + ENV_ALLOWED_HOSTS))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'cloudinary',
    'menu',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
    secure=True
)








# Notification Configuration
SLACK_WEBHOOK_URL = config('SLACK_WEBHOOK_URL', default='')
# Legacy email settings removed; using Slack webhook for notifications.






# CORS Configuration
DEFAULT_CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:5174', 
    'http://localhost:5175',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:5174',
    'http://127.0.0.1:5175',
    'https://amritha-heritage-admin-dashboard-e1.vercel.app',
    'https://www.amrithaheritage.com',
    'https://amrithaheritage.com',
]

ENV_CORS_ALLOWED_ORIGINS = [
    h.strip() for h in config('CORS_ALLOWED_ORIGINS', default='').split(',') if h.strip()
]

CORS_ALLOWED_ORIGINS = list(dict.fromkeys(DEFAULT_CORS_ALLOWED_ORIGINS + ENV_CORS_ALLOWED_ORIGINS))
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

# Additional CORS settings for better compatibility
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# CSRF trusted origins (merge env and defaults)
DEFAULT_CSRF_TRUSTED_ORIGINS = [
    'https://amrithaheritage.com',
    'https://www.amrithaheritage.com',
    'https://amritha-heritage-admin-dashboard-e1.vercel.app',
    'https://*.onrender.com',
]
ENV_CSRF_TRUSTED_ORIGINS = [
    h.strip() for h in config('CSRF_TRUSTED_ORIGINS', default='').split(',') if h.strip()
]
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(DEFAULT_CSRF_TRUSTED_ORIGINS + ENV_CSRF_TRUSTED_ORIGINS))



REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}




ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'




# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import dj_database_url

# PostgreSQL configuration with internal/external URL support
def get_database_config():
    # Try internal URL first (faster within Render network)
    internal_url = config('DATABASE_INTERNAL_URL', default=None)
    if internal_url:
        return dj_database_url.parse(internal_url, conn_max_age=600)
    
    # Fallback to external URL
    external_url = config('DATABASE_URL', default=None)
    if external_url:
        return dj_database_url.parse(external_url, conn_max_age=600)
    
    # Local development fallback
    return dj_database_url.parse('sqlite:///' + str(BASE_DIR / 'db.sqlite3'))

DATABASES = {
    'default': get_database_config()
}



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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
