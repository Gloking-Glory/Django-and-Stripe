from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'amount', 'currency', 'status', 'stripe_payment_intent_id',
        'content_type', 'content_object', 'stripe_session_id', 'receipt_url',
        'metadata', 'idempotency_key', 'created_at', 'updated_at', 'object_id'
    )
    list_filter = ('id', 'amount', 'currency', 'status', 'created_at')
    search_fields = ('id', 'content_type', 'object_id')
