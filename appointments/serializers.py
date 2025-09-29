from rest_framework import serializers
from django.utils import timezone
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    content_reformat_obj = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = (
            'id', 'provider_name', 'appointment_time', 'client_email',
            'amount', 'created_at', 'updated_at', 'content_reformat_obj'
        )

    def get_content_reformat_obj(self, obj):
        return {
            "id": str(obj.id),
            "email": obj.client_email,
            "created_at": obj.created_at.isoformat(),
        }

    def validate_appointment_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Appointment time cannot be in the past")
        return value
