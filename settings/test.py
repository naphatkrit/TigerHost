from settings.dev import *  # NOQA

ROOT_URLCONF = 'test_urls'

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'testdb.sqlite3'),
}
