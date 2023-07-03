# pylint: disable=missing-class-docstring,too-few-public-methods,unused-argument
import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "1234")


class SuperUserFactory(UserFactory):
    @factory.post_generation
    def set_properties(self, create, extracted, **kwargs):
        self.is_staff = True
        self.is_superuser = True
