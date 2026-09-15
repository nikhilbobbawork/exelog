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
        blank=True,
        help_text="Unique tracking identifier (e.g., TRK-984210)"
    )
    
    # Structured Destination Address Fields
    destination_address = models.CharField(
        max_length=255,
        help_text="Formatted address string from map selection"
    )
    destination_city = models.CharField(max_length=100, blank=True, default='')
    destination_postal_code = models.CharField(max_length=20, blank=True, default='')
    destination_country = models.CharField(max_length=100, blank=True, default='')

    # Spatial Coordinates for Map Rendering & Distance Routing
    destination_lat = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="Latitude coordinate (e.g. 40.712800)"
    )
    destination_lng = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text="Longitude coordinate (e.g. -74.006000)"
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
            self.tracking_number = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_number} - {self.destination_address} ({self.status})"