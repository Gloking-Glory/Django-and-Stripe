from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointments.views import AppointmentViewSet

router = DefaultRouter()
router.register('', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', include(router.urls)),
]
