"""
Django settings for project4 project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import environ

from .common import *

env = environ.Env()

env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "V1Kfqy/anrYCOkaJqDTSB5Z5rkAR38ln09KPYWixG34=",
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "") != "False"

ALLOWED_HOSTS = [
    "*",
]


ROOT_URLCONF = "project4.urls"

WSGI_APPLICATION = "project4.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES["default"].update(
    NAME=env.str("RDS_DB_NAME"),
    USER=env.str("RDS_DB_USER"),
    PASSWORD=env.str("RDS_DB_PASSWORD"),
    HOST=env.str("RDS_DB_HOST"),
    PORT=env.str("RDS_DB_PORT"),
)

AUTH_USER_MODEL = "network.User"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


SITE_ID = 1


# ------------------------------------------------------------------------------
# EMAIL SETTINGS
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.int("EMAIL_HOST_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_HOST_USE_TLS")
DEFAULT_FROM_EMAIL = env.str(
    "DEFAULT_FROM_EMAIL",
    "no-reply@cs50w-network-backend.com",
)
SERVER_EMAIL = env.str("SERVER_EMAIL", DEFAULT_FROM_EMAIL)
