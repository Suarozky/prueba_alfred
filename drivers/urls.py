from django.urls import path
from .views import DriverViews,  CreateDriver, UpdateDriver, DeleteDriver

urlpatterns = [
    path('drivers/', DriverViews.as_view(), name='driver-views'),
    path('drivers/create/', CreateDriver.as_view(), name='create-driver'),
    path('drivers/<int:pk>/update/', UpdateDriver.as_view(), name='update-driver'),
    path('drivers/<int:pk>/delete/', DeleteDriver.as_view(), name='delete-driver'),
]
