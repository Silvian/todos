"""Factories for api todo tests."""

import factory
from django_common.auth_backends import User

from factory.django import DjangoModelFactory

from api.models import Todo


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    username = factory.Faker('name')

    class Meta:
        model = User


class TodoFactory(DjangoModelFactory):
    """Factory for todos."""

    task = factory.Faker('sentence')
    due_date = factory.Faker('date_this_year')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Todo
