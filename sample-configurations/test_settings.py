SECRET_KEY = 'test_key'
DEBUG = False
ALLOWED_HOSTS = ['test.pigeon.latinier.fr']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
