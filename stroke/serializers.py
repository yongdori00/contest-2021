from rest_framework import serializers
from .models import *


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUploadModel
        fields = '__all__'
