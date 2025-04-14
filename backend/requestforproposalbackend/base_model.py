from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(default="system", max_length=100)
    updated_by = models.CharField(default="system", max_length=100)

    class Meta:
        abstract = True
