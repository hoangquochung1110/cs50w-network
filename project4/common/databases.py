# ------------------------------------------------------------------------------
# DATABASES - PostgreSQL
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# ------------------------------------------------------------------------------

DATABASES = dict(
    default=dict(
        ENGINE="django.db.backends.postgresql",
        ATOMIC_REQUESTS=True,
        CONN_MAX_AGE=600,
    ),
)
