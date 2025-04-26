from django.urls import path
from .views import TripCreateView, TripListView, TripRetrieveView, TripStatusUpdateView

urlpatterns = [

    path('trips/', TripListView.as_view(), name='trip-list'),
    path('trips/create/', TripCreateView.as_view(), name='trip-create'),
    path('trips/<int:trip_id>/', TripRetrieveView.as_view(), name='trip-detail'),
    path('trips/driver/<uuid:driverId>/status/', TripStatusUpdateView.as_view(), name='trip-status-update'),
]