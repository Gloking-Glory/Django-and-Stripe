from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'appointment_time', 'client_email', 'amount', 'created_at', 'updated_at')
    list_filter = ('appointment_time', 'created_at')
    search_fields = ('provider_name', 'client_email')
