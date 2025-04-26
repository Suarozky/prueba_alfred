# utils.py
from django.conf import settings
import requests
from ..models import Drivers
from ..serializers import DriverSerializer

from decouple import config

def find_nearest_driver(user):
    """
    Encuentra el conductor más cercano a un usuario.
    
    Args:
        user: El objeto usuario con coordenadas en el campo address
        
    Returns:
        dict: Información del conductor más cercano con detalles de ruta o None si no se encuentra
    """
    user_coords = user.address
    print(f"Coordenadas del usuario: {user_coords}")
    
    # Obtener todos los conductores
    drivers = Drivers.objects.all()
    
    if not drivers or not user_coords:
        return None
    
    # Convertir el string de coordenadas del usuario a una lista [longitud, latitud]
    try:
        lat, lng = map(float, user_coords.split(','))
        user_coords_list = [lng, lat]
    except Exception as e:
        print(f"Error al procesar coordenadas del usuario: {e}")
        return None
    
    nearest_driver = None
    min_distance = float('inf')
    route_info = None
    
    # Buscar el conductor más cercano
    for driver in drivers:
        driver_coords = driver.initial_address
        
        if not driver_coords:
            continue
            
        try:
            driver_lat, driver_lng = map(float, driver_coords.split(','))
            driver_coords_list = [driver_lng, driver_lat]
            
            current_route = get_route(user_coords_list, driver_coords_list)
            if not current_route:
                continue
                
            current_distance = current_route['distance']
            
            if current_distance < min_distance:
                min_distance = current_distance
                nearest_driver = driver
                route_info = current_route
        except Exception as e:
            print(f"Error al procesar coordenadas del conductor {driver.id}: {e}")
            continue
    
    if not nearest_driver:
        return None
    
    # Calcular el tiempo estimado (en minutos)
    estimated_arrival = round(route_info['duration'] / 60)
    
    # Calcular el precio estimado
    distance_km = round(min_distance / 1000)
    price = 10 + (distance_km * 2)
    
    # Serializar el conductor más cercano
    driver_serializer = DriverSerializer(nearest_driver)
    
    result = {
        "driver": driver_serializer.data,
        "estimated_arrival": estimated_arrival,  # minutos
        "price": round(price, 2),  # precio en la moneda local
        "distance_km": distance_km  # distancia en km
    }
    
    return result

def get_route(origin_coords, destination_coords):
    """Calcula la ruta entre dos puntos usando Mapbox Directions API"""
    try:
        mapbox_api_key = config('MAPBOX_API_KEY')
        
        origin = f"{origin_coords[0]},{origin_coords[1]}"
        destination = f"{destination_coords[0]},{destination_coords[1]}"
        
        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{origin};{destination}?access_token={mapbox_api_key}&geometries=geojson"
        
        response = requests.get(url)
        data = response.json()
        
        if 'routes' in data and len(data['routes']) > 0:
            route = data['routes'][0]
            return {
                'distance': route['distance'],
                'duration': route['duration'],
                'geometry': route['geometry']
            }
        return None
    except Exception as e:
        print(f"Error al calcular la ruta: {e}")
        return None