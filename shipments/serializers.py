from rest_framework import serializers
from .models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    # Format status display label for easy frontend rendering in Vue (e.g., "In Transit")
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'id',
            'tracking_number',
            'destination_address',
            'destination_city',
            'destination_postal_code',
            'destination_country',
            'destination_lat',
            'destination_lng',
            'driver_name',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_tracking_number(self, value):
        """Ensure tracking numbers are trimmed, uppercase, and non-empty if provided."""
        cleaned = value.strip().upper()
        if not cleaned:
            raise serializers.ValidationError("Tracking number cannot be blank.")
        return cleaned

    def validate_driver_name(self, value):
        """Clean up optional driver name input."""
        return value.strip() if value else value

    def validate_destination_address(self, value):
        """Ensure destination address is non-empty after trimming."""
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Destination address cannot be blank.")
        return cleaned