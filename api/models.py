"""Todo api object models."""
import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_common.auth_backends import User

from rest_framework.authtoken.models import Token


class Todo(models.Model):
    """Todo object model class."""

    task = models.TextField()
    created_date = models.DateField(
        default=datetime.date.today,
    )
    due_date = models.DateField(
        null=True,
        blank=True,
    )
    completed = models.BooleanField(
        default=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def publish(self):
        """Set created date to be now."""
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.task


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate authentication API token for a created user instance."""
    if created:
        Token.objects.create(user=instance)
