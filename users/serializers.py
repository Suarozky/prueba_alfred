from rest_framework import serializers, status 
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.authtoken.models import Token
from .models import User



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone', 'password']

    def create(self, validated_data):  # <-- FUERA de Meta
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Aquí sí hasheas bien la contraseña
        user.save()
        return user
