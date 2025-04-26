# ride/models.py
from django.db import models
from constants.statusTrip import Status
from django.conf import settings
import uuid
from drivers.models import Drivers


class Trip(models.Model):
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Usa esta referencia
        on_delete=models.CASCADE
    )
    driver = models.ForeignKey('drivers.Drivers', on_delete=models.CASCADE)  
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    estimated_arrival = models.DurationField(help_text="Estimated time to arrive (hh:mm:ss)")
    distance_km = models.IntegerField(help_text="Distance of the ride in kilometers")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"
