from settings.dev import *  # NOQA

ROOT_URLCONF = 'test_urls'

if 'aws_db_addons' not in INSTALLED_APPS:
    INSTALLED_APPS.append('aws_db_addons')

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'testdb.sqlite3'),
}

PAAS_BACKENDS['test_backend'] = {
    'API_URL': 'http://fake.example.com',
    'CLIENT': 'api_server.clients.base_client.BaseClient',
}

ADDON_PROVIDERS['test_provider'] = {
    'CLASS': 'api_server.addons.providers.base_provider.BaseAddonProvider',
}

DEFAULT_PAAS_BACKEND = 'test_backend'

# turn all async tasks into blocking tasks
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
