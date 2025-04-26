from rest_framework import serializers
from .models import Drivers


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = ['id', 'user', 'initial_address', 'cedula']