import uuid
from django.db import models
from core.models import TimeStampedModel


class Shipment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
        DELIVERED = 'DELIVERED', 'Delivered'

    tracking_number = models.CharField(
        max_length=50, 
        unique=True, 
        db_index=True,
        blank=True,  # Allows auto-generation on create
        help_text="Unique tracking identifier (e.g., TRK-984210)"
    )
    destination = models.TextField(
        help_text="Full delivery address"
    )
    driver_name = models.CharField(
        max_length=100, 
        blank=True, 
        default='', 
        help_text="Name of assigned driver or empty string if unassigned"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING,
        db_index=True
    )

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Auto-generate a tracking number if not explicitly provided."""
        if not self.tracking_number:
            # Generates format like: TRK-A1B2C3D4
            self.tracking_number = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_number} - {self.status}"