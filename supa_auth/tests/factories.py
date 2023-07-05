# pylint: disable=missing-class-docstring,too-few-public-methods,unused-argument
import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory.fuzzy import FuzzyDateTime


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "1234")
    email_confirmed_at = FuzzyDateTime(
        timezone.now() - timezone.timedelta(days=30), timezone.now()
    )


class SuperUserFactory(UserFactory):
    @factory.post_generation
    def set_properties(self, create, extracted, **kwargs):
        self.is_staff = True
        self.is_superuser = True
