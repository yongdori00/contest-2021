from rest_framework import serializers
from .models import *


class MiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mise
        fields = '__all__'
