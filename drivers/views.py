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
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class DriverViews(APIView):
    """
    View para listar todos los conductores (drivers)
    """

    def get(self, request):
        """
        Método GET para obtener todos los drivers
        """
        drivers = Drivers.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)


class DriverMixin:
    """
    Mixin para obtener un driver por su primary key (pk)
    """

    def get_driver(self, pk):
        """
        Método para buscar un driver por pk
        """
        try:
            return Drivers.objects.get(pk=pk)
        except Drivers.DoesNotExist:
            return None


class UpdateDriver(DriverMixin, APIView):
    """
    View para actualizar información de un conductor específico
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(request=DriverSerializer)  # <-- Aquí agregamos el body para actualizar
    def put(self, request, pk):
        """
        Método PUT para actualizar un driver si pertenece al usuario autenticado
        """
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
    """
    View para eliminar un conductor específico
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """
        Método DELETE para eliminar un driver si pertenece al usuario autenticado
        """
        driver = self.get_driver(pk)
        if not driver:
            return Response({"error": "Driver no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if driver.user != request.user:
            return Response({"error": "No tienes permiso para eliminar este driver."}, status=status.HTTP_403_FORBIDDEN)

        driver.delete()
        return Response({"message": "Driver eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)


class CreateDriver(APIView):
    """
    View para crear un nuevo conductor asociado al usuario autenticado
    """
    permission_classes = [IsAuthenticated]  

    @extend_schema(
        request=DriverSerializer,
        examples=[
            OpenApiExample(
                name='driver_example',
                summary='Ejemplo de creación de driver',
                description='Ejemplo de los datos necesarios para crear un driver',
                value={
                    'initial_address': 'Calle 123, Ciudad',
                    'cedula': '1234567890'
                },
                request_only=True,
            )
        ],
        description='Crea un nuevo driver asociado al usuario autenticado'
    )
    def post(self, request):
        """
        Método POST para crear un nuevo driver
        """
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
