# shipments/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Shipment  # <--- Import the model from models.py


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    """Admin configuration for managing shipments in Exelog."""

    list_display = (
        'tracking_number',
        'destination_short',
        'driver_name_display',
        'status_badge',
        'created_at',
        'updated_at',
    )

    list_filter = ('status', 'created_at')
    search_fields = ('tracking_number', 'destination', 'driver_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_in_transit', 'mark_as_delivered', 'mark_as_pending']

    # --- Custom Column Renderers ---

    @admin.display(description='Destination')
    def destination_short(self, obj):
        if len(obj.destination) > 40:
            return f"{obj.destination[:37]}..."
        return obj.destination

    @admin.display(description='Driver')
    def driver_name_display(self, obj):
        return obj.driver_name if obj.driver_name else format_html('<span style="color: #999;">Unassigned</span>')

    @admin.display(description='Status')
    def status_badge(self, obj):
        badge_styles = {
            Shipment.Status.PENDING: 'background-color: #fef3c7; color: #92400e; border: 1px solid #fcd34d;',
            Shipment.Status.IN_TRANSIT: 'background-color: #dbeafe; color: #1e40af; border: 1px solid #93c5fd;',
            Shipment.Status.DELIVERED: 'background-color: #d1fae5; color: #065f46; border: 1px solid #6ee7b7;',
        }
        style = badge_styles.get(obj.status, 'background-color: #f3f4f6; color: #374151;')
        return format_html(
            '<span style="padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px; {}">{}</span>',
            style,
            obj.get_status_display()
        )

    # --- Bulk Admin Actions ---

    @admin.action(description='Mark selected shipments as In Transit')
    def mark_as_in_transit(self, request, queryset):
        updated = queryset.update(status=Shipment.Status.IN_TRANSIT)
        self.message_user(request, f"{updated} shipment(s) marked as In Transit.")

    @admin.action(description='Mark selected shipments as Delivered')
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status=Shipment.Status.DELIVERED)
        self.message_user(request, f"{updated} shipment(s) marked as Delivered.")

    @admin.action(description='Mark selected shipments as Pending')
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status=Shipment.Status.PENDING)
        self.message_user(request, f"{updated} shipment(s) marked as Pending.")