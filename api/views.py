"""Api rest framework view sets."""

from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from api.serializers import TodoSerializer
from .models import Todo


class TodoViewSet(viewsets.ModelViewSet, RetrieveUpdateDestroyAPIView):
    """
    Todo list view set.

    Allows listing, retrieving, updating and deleting a todo item
    for the authenticated request user.
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_fields = ('completed', )

    def get_queryset(self):
        """Return the queryset of todos for this user."""
        return Todo.objects.filter(user=self.request.user)
