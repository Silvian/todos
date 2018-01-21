"""Api rest framework view sets."""

from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from api.serializers import TodoSerializer
from .models import Todo


class TodoViewSet(viewsets.ModelViewSet, RetrieveUpdateDestroyAPIView):
    """
    Todo list item view set.
    Setting the query set and the serializer.
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_fields = ('completed', )

    def get_queryset(self):
        """Return the queryset of todos for this user."""
        return Todo.objects.filter(user=self.request.user)
