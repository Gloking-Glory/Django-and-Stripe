import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Payment(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idempotency_key = models.CharField(max_length=36, unique=True, editable=False, default=lambda: str(uuid.uuid4()))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=200, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=10, default='usd')
    status = models.CharField(max_length=30, choices=status_choices, default='pending')
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    receipt_url = models.URLField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['content_type', 'object_id']), models.Index(fields=['stripe_payment_intent_id'])]

    def __str__(self):
        return f"{self.id} — {self.created_at:%Y-%m-%d %H:%M}"
