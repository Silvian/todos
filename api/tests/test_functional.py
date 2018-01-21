"""Todo api functional test cases."""

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Todo
from api.tests import UserFactory, TodoFactory


class TestTodoFunctionalTestCase(APITestCase):
    """Todo model api functional tests."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_superuser=True)
        cls.todo = TodoFactory(user=cls.user)

    def test_user_can_read_todo_items(self):
        """Test that a user can read todo items."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/todos/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(self.todo.id, response.data[0]['id'])
        self.assertEqual(self.todo.created_date.strftime('%Y-%m-%d'), response.data[0]['created_date'])
        self.assertEqual(self.todo.task, response.data[0]['task'])
        self.assertEqual(self.todo.due_date.strftime('%Y-%m-%d'), response.data[0]['due_date'])
        self.assertEqual(self.todo.completed, response.data[0]['completed'])

    def test_user_can_create_todo_item(self):
        """Test that a user can create todo item."""
        new_todo = TodoFactory(user=self.user)
        self.client.force_authenticate(user=self.user)

        # clean todo already created as part of factory
        Todo.objects.get(id=new_todo.id).delete()

        response = self.client.post(
            "/api/todos/",
            data={
                "task": new_todo.task,
                "due_date": new_todo.due_date.strftime('%Y-%m-%d'),
                "completed": new_todo.completed,
            },
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(new_todo.created_date.strftime('%Y-%m-%d'), response.data['created_date'])
        self.assertEqual(new_todo.task, response.data['task'])
        self.assertEqual(new_todo.due_date.strftime('%Y-%m-%d'), response.data['due_date'])
        self.assertEqual(new_todo.completed, response.data['completed'])

        # check that there are now two items in the todo list for this user
        response = self.client.get("/api/todos/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEquals(2, len(response.data))

    def test_user_can_update_todo_item(self):
        """Test that a user can update a todo item."""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            "/api/todos/{}/".format(self.todo.id),
            data={
                "completed": True,
            },
            format='json',
        )

        # Retrieve the newly updated todo item
        todo = Todo.objects.get(id=self.todo.id)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(todo.created_date.strftime('%Y-%m-%d'), response.data['created_date'])
        self.assertEqual(todo.task, response.data['task'])
        self.assertEqual(todo.due_date.strftime('%Y-%m-%d'), response.data['due_date'])
        self.assertEqual(todo.completed, response.data['completed'])

    def test_user_can_delete_todo_item(self):
        """Test that a user can delete a todo item."""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            "/api/todos/{}/".format(self.todo.id),
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        # Retrieve the todo list check that the list has no items
        response = self.client.get("/api/todos/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEquals(0, len(response.data))

    def test_another_user_cannot_view_or_edit_todo_items(self):
        """Test that another user cannot read the todo items."""
        another_user = UserFactory()
        another_todo = TodoFactory(user=self.user)  # create another todo for the existing user
        self.client.force_authenticate(user=another_user)

        # Retrieve list of todos
        response = self.client.get("/api/todos/")

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK,
        )

        # List should be empty since the todo previously created does not belong to this user
        self.assertEquals(0, len(response.data))

        response = self.client.post(
            "/api/todos/",
            data={
                "task": another_todo.task,
                "due_date": another_todo.due_date.strftime('%Y-%m-%d'),
                "completed": another_todo.completed,
            },
            format='json',
        )

        # Should not be allowed to POST
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        response = self.client.patch(
            "/api/todos/{}/".format(another_todo.id),
            data={
                "completed": True,
            },
            format='json',
        )

        # Should not be allowed to PATCH
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Should not be allowed to DELETE
        esponse = self.client.delete(
            "/api/todos/{}/".format(self.todo.id),
            format='json',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
