from django.contrib.contenttypes.models import ContentType
from .models import Payment

def create_payment_obj(model_obj):
    content_type = ContentType.objects.get_for_model(model_obj)
    amount = max(int(getattr(model_obj, "amount", 0) * 100), 100)

    payment_obj = Payment.objects.create(
        content_type=content_type,
        object_id=str(model_obj.id),
        amount=amount,
        currency="usd",
        status="pending"
    )

    return payment_obj
