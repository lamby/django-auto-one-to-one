from django.contrib.auth.models import User
from django.test import TestCase

from .models import Brim, Hat, Profile


class SmokeTests(TestCase):
    def test_model_creation(self):
        # type: () -> None

        trilby = Hat(name="Trilby")

        self.assertFalse(Brim.objects.exists())

        trilby.save()

        trilby_brim = Brim.objects.get()

        self.assertEqual(trilby_brim, trilby.brim)
        self.assertEqual(trilby_brim.hat, trilby)

    def test_str(self):
        # type: () -> None

        trilby = Hat.objects.create(name="Trilby")

        self.assertIn("Trilby", str(trilby.brim))

    def test_two_models(self):
        # type: () -> None

        trilby = Hat.objects.create(name="Trilby")
        fedora = Hat.objects.create(name="Fedora")

        self.assertNotEqual(fedora.brim, trilby.brim)
        self.assertEqual(2, Brim.objects.count())

    def test_model_deletion(self):
        # type: () -> None

        trilby = Hat.objects.create(name="Trilby")

        self.assertTrue(Brim.objects.exists())

        trilby.delete()

        self.assertFalse(Brim.objects.exists())

    def test_per_user_data(self):
        # type: () -> None

        user = User.objects.create()
        profile = Profile.objects.get()

        self.assertEqual(profile, user.profile)
        self.assertEqual(profile.user, user)
