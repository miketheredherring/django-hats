# What backend authenticators do we check against?
AUTHENTICATION_BACKENDS = (
    # Standard Django auth
    'django.contrib.auth.backends.ModelBackend',
)

DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_hats',
    'tests',
]

ROOT_URLCONF = 'tests.urls'

SITE_ID = 1

SECRET_KEY = 'faffing-about-falafels'

MIDDLEWARE_CLASSES = []
