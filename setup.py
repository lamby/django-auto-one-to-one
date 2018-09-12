from setuptools import setup

setup(
    name='django-auto-one-to-one',
    version='3.0.0',
    packages=(
        'django_auto_one_to_one',
    ),
    url='https://chris-lamb.co.uk/projects/django-auto-one-to-one',
    author="Chris Lamb",
    author_email="chris@chris-lamb.co.uk",
    description="Automatically create and destroy child model instances",

    install_requires=(
        'Django>=1.8',
        'six',
    ),
)
