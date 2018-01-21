"""Api django rest framework serializers."""

from rest_framework import serializers

from api.models import Todo


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    """Todo model serializer."""

    class Meta:
        model = Todo

        read_only_fields = (
            'id',
            'created_date',
        )

        fields = read_only_fields + (
            'task',
            'due_date',
            'completed',
        )

    def validate(self, attrs):
        """Add or update a todo item for authenticated user."""
        request_user = self.context['request'].user
        attrs['user'] = request_user
        return super().validate(attrs)
