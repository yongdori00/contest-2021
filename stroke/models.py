import datetime

from django.db import models
from django.utils import timezone

class ImageUploadModel(models.Model):
    description = models.CharField(max_length=255, blank=True, null = True)
    document = models.TextField(null = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)