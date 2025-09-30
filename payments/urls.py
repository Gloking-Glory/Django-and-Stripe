from django.urls import path
from .views import CreatePaymentIntentView, CreateCheckoutSessionView, PaymentListView, PaymentDetailView, PaymentUpdateView, PaymentDeleteView

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('<uuid:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('detail/', PaymentDetailView.as_view(), name="payment-detail"),
    path('<uuid:pk>/update/', PaymentUpdateView.as_view(), name='payment-update'),
    path('<uuid:pk>/delete/', PaymentDeleteView.as_view(), name='payment-delete'),
]
