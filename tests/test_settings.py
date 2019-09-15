SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tests',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

# Tell Django to ignore migrations and create these apps' tables from the models
# instead. This is needed in Django >= 2.2, where something changed such that if
# the tables for our models (which don't have migrations) reference the tables
# for contrib models (which do have migrations) then the creation of our tables
# as part of the test setup fails.
MIGRATION_MODULES = {x: None for x in ('auth', 'contenttypes')}
