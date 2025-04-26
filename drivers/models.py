from django.db import models
import uuid
from users.models import User

class Drivers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    initial_address = models.CharField(max_length=255, blank=True)
    cedula = models.IntegerField(unique=True, blank=True, null=True)  # Agregué null=True por si acaso

    def __str__(self):
        return self.user.email