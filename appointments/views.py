from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        now = timezone.now()
        upcoming_appointment = now + timedelta(days=1000)
        queryset = Appointment.objects.filter(
            appointment_time__gte=now,
            appointment_time__lte=upcoming_appointment
        )

        params = self.request.query_params

        appointment_id = params.get("id")
        if appointment_id:
            queryset = queryset.filter(id=appointment_id)

        appointment_time = params.get("appointment_time")
        if appointment_time:
            queryset = queryset.filter(appointment_time=appointment_time)
        
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment_obj = serializer.save()

        return Response(
            {
                "message": "Appointment created successfully",
                "data": {
                    "id": appointment_obj.id,
                    "provider_name": appointment_obj.provider_name,
                    "appointment_time": appointment_obj.appointment_time
                },
            },
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "message": "Appointment List",
            "data": {
                "appointment_lists": serializer.data,
            }
        })

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)

        return Response({
            "message": "Appointment Found",
            "data": {
                "appointment_detail": serializer.data,
            }
        })

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)

        if "appointment_time" not in request.data:
            return Response(
                { "error": "Only appointment_time can be updated" },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.is_valid(raise_exception=True)
        appointment_obj = serializer.save()

        return Response(
            {
                "message": "Appointment time updated successfully",
                "data": {
                    "id": appointment_obj.id,
                    "appointment_time": appointment_obj.appointment_time,
                    "appointment_detail": serializer.data
                }
            }, 
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()

        return Response(
            { "message": "Appointment deleted successfully" },
            status=status.HTTP_204_NO_CONTENT
        )
