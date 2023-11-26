# pylint: disable=missing-class-docstring,too-few-public-methods,unused-argument
import factory
from testapp.models import Profile

from supa_auth.tests.factories import UserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    preferred_username = factory.Faker("user_name")
