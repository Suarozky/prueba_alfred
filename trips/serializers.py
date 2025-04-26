from rest_framework import serializers
from .models import Trip
from constants.statusTrip import Status  # Asegúrate de que Status sea un Enum

class TripSerializer(serializers.ModelSerializer):
    
    # Establecemos el modelo y los campos que queremos exponer
    class Meta:
        model = Trip
        fields = ['id', 'user', 'driver', 'status', 'estimated_arrival', 'distance_km', 'price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # No queremos que esos campos sean modificables

    # Validación personalizada para el campo distance_km
    def validate_distance_km(self, value):
        if value < 0:
            raise serializers.ValidationError("Distance must be a positive number.")
        return value

    # Validación personalizada para el campo price
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    # Usar el Enum Status para validar o formatear el campo status
    def validate_status(self, value):
        if value not in Status:
            raise serializers.ValidationError(f"Invalid status: {value}.")
        return value
