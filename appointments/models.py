import uuid
from django.db import models

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    provider_name = models.CharField(max_length=200)
    appointment_time = models.DateTimeField()
    client_email = models.EmailField()
    amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider_name', 'appointment_time')
        ordering = ['appointment_time']
        indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
        return f"{self.provider_name} — {self.appointment_time:%Y-%m-%d %H:%M}"
