import datetime

from django.db import models
from django.utils import timezone

class ImageUploadModel(models.Model):
    description = models.CharField(max_length=255, blank=True, null = True)
    document = models.FileField(upload_to = 'images/', null = True)
    #document = models.ImageField(upload_to = 'images/', null = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)