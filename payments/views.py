import stripe
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from appointments.models import Appointment
from .models import Payment
from .helpers import create_payment_obj
from .serializers import PaymentSerializer
from django.shortcuts import get_object_or_404

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        appointment_id = request.data.get("appointment_id")
        appointment = Appointment.objects.get(id=appointment_id)

        payment_obj = create_payment_obj(appointment)

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=payment_obj.amount,
                currency=payment_obj.currency,
                metadata={
                    "payment_id": str(payment_obj.id),
                    "appointment_id": str(appointment.id),
                },
                idempotency_key=payment_obj.idempotency_key,
            )

        except stripe.error.StripeError as e:
            payment_obj.status = "failed"
            payment_obj.metadata = {"stripe_error": str(e)}
            payment_obj.save()

            return Response(
                { "error": "Stripe error creating payment intent" },
                status=status.HTTP_502_BAD_GATEWAY
            )

        payment_obj.stripe_payment_intent_id = payment_intent["id"]
        print(payment_intent)
        payment_obj.save()

        return Response(
            {
                "payment_id": str(payment_obj.id),
                "client_secret": payment_intent.get("client_secret"),
            },
            status=status.HTTP_201_CREATED,
        )


class CreateCheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        appointment_id = request.data.get("appointment_id")
        appointment = Appointment.objects.get(id=appointment_id)

        payment_obj = create_payment_obj(appointment)

        try:
            checkout_session = stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                success_url=settings.FRONTEND_SUCCESS_URL or request.build_absolute_uri("/payments/success/"),
                cancel_url=settings.FRONTEND_CANCEL_URL or request.build_absolute_uri("/payments/cancel/"),
                client_reference_id=str(appointment.id),

                metadata={
                    "payment_id": str(payment_obj.id),
                    "appointment_id": str(appointment.id)
                },

                line_items=[
                    {
                        "price_data": {
                            "currency": payment_obj.currency,
                            "unit_amount": payment_obj.amount,
                            "product_data": {
                                "name": f"Appointment with {appointment.provider_name}",
                                "description": f"Appointment Time: {appointment.appointment_time}, Email: {appointment.client_email}",
                            },
                        },
                        "quantity": 1,
                    }
                ],
            )

        except stripe.error.StripeError as e:
            payment_obj.status = "failed"
            payment_obj.metadata = {"stripe_error": str(e)}
            payment_obj.save()

            return Response(
                { "error": "Stripe error creating checkout session" },
                status=status.HTTP_502_BAD_GATEWAY
            )

        payment_obj.stripe_session_id = checkout_session["id"]
        payment_obj.save()

        return Response(
            {
                "checkout_url": checkout_session.get("url")
            },
            status=status.HTTP_201_CREATED
        )

class PaymentListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Payment.objects.all().order_by("-created_at")
        serializer = PaymentSerializer(queryset, many=True)

        return Response(
            {
                "message": "Payment Lists",
                "data": {
                    "payment_lists": serializer.data,
                }
            },
            status=status.HTTP_200_OK
        )

class PaymentDetailView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Payment.objects.all()
        payment_id = request.query_params.get("id")
        payment_status = request.query_params.get("status")

        if payment_id:
            queryset = queryset.filter(id=payment_id)

        if payment_status:
            queryset = queryset.filter(status=payment_status)

        if not queryset.exists():
            return Response(
                {"error": "No payment found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PaymentSerializer(queryset, many=True)

        return Response(
            {
                "message": "Payment Found",
                "data": {
                    "payment_detail": serializer.data,
                }
            },
            status=status.HTTP_200_OK
        )

class PaymentUpdateView(APIView):
    def patch(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs["pk"])
        allowed_fields = {"amount", "currency", "status"}
        updated_data = {key: value for key, value in request.data.items() if key in allowed_fields}

        if not updated_data:
            return Response(
                { "error": "Only 'amount', 'currency' or 'status' can be updated." },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PaymentSerializer(payment, data=updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response (
            {
                "message": "Payment updated successfully",
                "data": {
                    "payment_detail": serializer.data
                }
            },
            status=status.HTTP_200_OK
        )

class PaymentDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs["pk"])
        payment.delete()

        return Response(
            { "message": "Payment deleted successfully" },
            status=status.HTTP_200_OK
        )