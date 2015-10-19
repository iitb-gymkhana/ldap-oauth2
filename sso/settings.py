"""
Django settings for sso project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import logging.config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import ldap
from django_auth_ldap.config import LDAPSearch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Authentication Backends
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# LDAP Server URI
# http://pythonhosted.org/django-auth-ldap/authentication.html#server-config
AUTH_LDAP_SERVER_URI = "ldap://ldap.iitb.ac.in"

AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=iitb,dc=ac,dc=in",
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": 'mail',
}

AUTH_PROFILE_MODULE = 'account.UserProfile'

AUTH_LDAP_PROFILE_ATTR_MAP = {
    'description': 'description',
    'roll_number': 'employeeNumber',
    'type': 'employeeType',
    'mobile': 'mobile',
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'oauth2_provider',
    'account',
    'application',
    'user_resource',
    'core',
    'widget',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'sso.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sso.wsgi.application'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGIN_URL = 'account:login'

# TODO: Fix this! Use named url
LOGIN_REDIRECT_URL = 'user:home'

STATICFILES_DIRS = (
    # Add all static files here. use os.path.join(BASE_DIR, 'your/staticfile/path')
    os.path.join(BASE_DIR, 'static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

OAUTH2_PROVIDER_APPLICATION_MODEL = 'application.Application'

OAUTH2_PROVIDER = {
    'SCOPES': {
        'basic': 'Know who you are on this site',
        'profile': 'Basic profile information which includes first_name and last_name',
        'picture': 'Profile picture',
        'ldap': 'Your ldap information which includes your ldap username and email',
        'phone': 'Your contact number including additional numbers',
        'insti_address': 'Your address inside institute',
        'program': 'Your roll number, department, course, joining year and graduation year',
        'secondary_emails': 'Your alternate emails',
        'send_mail': 'Send email to you via SSO',
    },
    'OAUTH2_VALIDATOR_CLASS': 'application.validators.CustomOAuth2Validator',
    'REQUEST_APPROVAL_PROMPT': 'auto',
}

OAUTH2_DEFAULT_SCOPES = [
    'basic',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] [%(name)s] [%(module)s] [Process:%(process)d] '
                      '[Thread:%(thread)d] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'suppress_deprecated_warnings': {
            '()': 'sso.filters.SuppressDeprecatedWarnings',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose'
        },
        'file_application': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/application.log'),
            'formatter': 'verbose',
            'filters': ['suppress_deprecated_warnings'],
        },
        'file_feed': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/feeds.log'),
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file_application'],
            'level': 'INFO',
        },
        'gcm': {
            'handlers': ['file_application'],
            'level': 'DEBUG',
        },
        'requests': {
            'handlers': ['file_application'],
            'level': 'WARNING',
        },
        'django': {
            'handlers': ['file_django', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'feed': {
            'handlers': ['file_feed'],
            'level': 'INFO',
            'propagate': False,
        },
    },

}
logging.config.dictConfig(LOGGING)

from settings_user import *
