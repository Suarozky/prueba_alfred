from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Drivers
from .serializers import DriverSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.conf import settings
from decouple import config
import requests

class DriverViews(APIView):
    def get(self, request):
        drivers = Drivers.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

class DriverMixin:
    def get_driver(self, pk):
        try:
            return Drivers.objects.get(pk=pk)
        except Drivers.DoesNotExist:
            return None

class UpdateDriver(DriverMixin, APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        driver = self.get_driver(pk)
        if not driver:
            return Response({"error": "Driver no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if driver.user != request.user:
            return Response({"error": "No tienes permiso para actualizar este driver."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteDriver(DriverMixin, APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        driver = self.get_driver(pk)
        if not driver:
            return Response({"error": "Driver no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if driver.user != request.user:
            return Response({"error": "No tienes permiso para eliminar este driver."}, status=status.HTTP_403_FORBIDDEN)

        driver.delete()
        return Response({"message": "Driver eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)

class CreateDriver(APIView):
    print(f"\n--- DEBUG ---")
    print("--------------\n")
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        print(f"\n--- DEBUG ---")
        print(f"Usuario autenticado: {request.user}")
        print(f"Token usado: {request.auth}")
        print(f"Headers: {request.headers}")
        print("--------------\n")
        user = request.user

        if Drivers.objects.filter(user=user).exists():
            return Response({"error": "Este usuario ya tiene un driver asociado."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['user'] = user.id  

        serializer = DriverSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



