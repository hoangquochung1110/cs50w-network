# Application definition

LOCAL_APPS = [
    "network",
]

DRF_PACKAGES = [
    "django_filters",
    "rest_framework",
    "drf_spectacular",
]

THIRD_PARTY = [
    "django_extensions",
    "whitenoise.runserver_nostatic",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

INSTALLED_APPS += LOCAL_APPS + DRF_PACKAGES + THIRD_PARTY
