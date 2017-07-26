SECRET_KEY = 'test_key'
DEBUG = False
ALLOWED_HOSTS = ['test.pigeon.latinier.fr']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pigeon',
        'USER': 'pigeon_test',
        'PASSWORD': 'test',
        'HOST': 'localhost',
        'POST': '',
    }
}
