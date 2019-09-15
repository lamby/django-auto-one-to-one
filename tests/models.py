from django.db import models
from django.contrib.auth.models import User

from django_auto_one_to_one import AutoOneToOneModel, PerUserData


class Hat(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        # type: () -> str
        return self.name


class Brim(AutoOneToOneModel(Hat)):
    pass


class Profile(PerUserData('profile')):
    nickname = models.CharField(max_length=20)
