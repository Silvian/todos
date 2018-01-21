"""Todo api models test cases."""

from unittest import TestCase

from django.utils import timezone

from api.tests import UserFactory, TodoFactory
from rest_framework.authtoken.models import Token


class TodoTestCase(TestCase):
    """Tests the todo model."""

    def setUp(self):
        self.todo = TodoFactory()

    def test_todo_model_created_date_is_now(self):
        """Test that todo model create new todo item."""
        date_now = timezone.now().date()

        self.assertEquals(self.todo.created_date, date_now)

    def test_todo_item_user_and_due_date_is_assigned(self):
        """Test that the todo item user is the assigned user."""
        user = UserFactory(username='some_user')
        todo_item = TodoFactory(
            user=user,
            due_date=timezone.now().date(),
        )

        self.assertEquals(todo_item.user, user)
        self.assertEquals(todo_item.due_date, timezone.now().date())

    def test_default_completed_value_is_false(self):
        """Test that the completed value is set to false by default."""
        self.assertFalse(self.todo.completed)

    def test_user_creation_generates_token(self):
        """Test that creating a new user generates a token for that user."""
        user = UserFactory(username='test_user')

        token = Token.objects.get(user=user)
        self.assertIsNotNone(token)
        self.assertEquals(token.user, user)
