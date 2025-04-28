from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from drivers.models import Drivers
from .models import Trip
from .serializers import TripSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drivers.service.nearest_driver import find_nearest_driver
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Definir el parámetro Authorization una sola vez
token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Token JWT Bearer. Formato: Bearer <token>",
    type=openapi.TYPE_STRING
)


class TripCreateView(APIView):
    """
    View para crear nuevos viajes con opción de asignar automáticamente el conductor más cercano
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[token_param],
        request_body=TripSerializer,
        responses={201: TripSerializer}
    )
    def post(self, request):
        data = request.data.copy()
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        driver_id = data.get('driver')
        driver_info = None

        if driver_id:
            try:
                driver = Drivers.objects.get(id=driver_id)
            except Drivers.DoesNotExist:
                return Response(
                    {"error": "Driver with the provided ID does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            driver_info = find_nearest_driver(user)

            if not driver_info:
                return Response(
                    {"error": "No se encontró ningún conductor cercano disponible."},
                    status=status.HTTP_404_NOT_FOUND
                )

            driver_id = driver_info["driver"]["id"]
            try:
                driver = Drivers.objects.get(id=driver_id)
            except Drivers.DoesNotExist:
                return Response(
                    {"error": "Error al encontrar el conductor más cercano."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        data['user'] = user.id
        data['driver'] = driver.id
        data['status'] = 'in_progress'

        if driver_info:
            data['estimated_arrival'] = driver_info["estimated_arrival"]
            data['distance_km'] = driver_info["distance_km"]
            data['price'] = driver_info["price"]
        else:
            data['estimated_arrival'] = getattr(driver, 'estimated_arrival', 15)
            data['distance_km'] = getattr(driver, 'distance_km', 5.0)
            data['price'] = getattr(driver, 'price', 20.0)

        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            viaje = serializer.save()
            return Response(TripSerializer(viaje).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripListView(APIView):
    """
    View para listar todos los viajes
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[token_param],
        responses={200: TripSerializer(many=True)}
    )
    def get(self, request):
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)


class TripRetrieveView(APIView):
    """
    View para obtener un viaje específico
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            token_param,
            openapi.Parameter(
                'trip_id',
                openapi.IN_PATH,
                description="ID del viaje a recuperar",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: TripSerializer, 404: 'Trip not found'}
    )
    def get(self, request, trip_id):
        try:
            trip = Trip.objects.get(id=trip_id)
            serializer = TripSerializer(trip)
            return Response(serializer.data)
        except Trip.DoesNotExist:
            return Response(
                {"error": "Trip not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class TripStatusUpdateView(APIView):
    """
    View para actualizar el estado de un viaje en progreso
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            token_param,
            openapi.Parameter(
                'driverId',
                openapi.IN_PATH,
                description="ID del conductor que tiene el viaje en progreso",
                type=openapi.TYPE_STRING
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Nuevo estado: 'completed' o 'cancelled'",
                    enum=['completed', 'cancelled']
                )
            }
        ),
        responses={200: TripSerializer, 404: 'No trip found for driver'}
    )
    def patch(self, request, driverId):
        new_status = request.data.get('status', 'COMPLETED')

        if new_status not in ['completed', 'cancelled']:
            return Response(
                {"error": "Invalid status. Only COMPLETED or CANCELLED allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        trips = Trip.objects.filter(driver=driverId, status='in_progress').first()

        if trips:
            trips.status = new_status
            trips.save()
            serializer = TripSerializer(trips)
            return Response(serializer.data)

        return Response(
            {"error": f"No se encontró ningún viaje en progreso para el conductor con ID {driverId}"},
            status=status.HTTP_404_NOT_FOUND
        )
