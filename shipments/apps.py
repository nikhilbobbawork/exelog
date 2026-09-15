from django.apps import AppConfig


class ShipmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shipments'
    verbose_name = 'Shipment Management'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        Uncomment the line below if you add a signals.py file.
        """
        # import shipments.signals  # noqa