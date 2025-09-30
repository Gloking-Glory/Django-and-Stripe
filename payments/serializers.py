from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    content_reformat_obj = serializers.SerializerMethodField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            'id', 'content_type', 'object_id', 'content_object', 'amount', 
            'currency', 'status', 'stripe_payment_intent_id', 'stripe_session_id',
            'receipt_url', 'metadata', 'idempotency_key', 'created_at', 'updated_at', 'content_reformat_obj'
        )
        read_only_fields = ('stripe_payment_intent_id', 'stripe_session_id', 'receipt_url', 'created_at', 'updated_at')

    def get_content_reformat_obj(self, obj):
        return {
            "id": str(obj.id),
            "status": obj.status,
            "created_at": obj.created_at.isoformat(),
        }
    
    def get_content_object(self, obj):
        if obj.content_type:
            return {
                "id": str(getattr(obj.content_object, "id", "")),
                "type": obj.content_type.name if obj.content_type else None,
                "repr": str(obj.content_object),
            }
        return None
