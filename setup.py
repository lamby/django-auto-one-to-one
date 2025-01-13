#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name='django-auto-one-to-one',
    version='3.3.6',
    packages=find_packages(exclude=('tests',)),

    url='https://chris-lamb.co.uk/projects/django-auto-one-to-one',
    author="Chris Lamb",
    author_email="chris@chris-lamb.co.uk",
    description="Automatically create and destroy child model instances",

    install_requires=(
        'Django>=1.11',
    ),
)
