from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        


class User(AbstractUser):
    ROLE_CHOICES = [
        ('DISPATCHER', 'Dispatcher'),
        ('DRIVER', 'Driver'),
        ('MANAGER', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='DISPATCHER')