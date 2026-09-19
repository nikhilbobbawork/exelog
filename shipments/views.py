from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Shipment, Driver
from .serializers import ShipmentSerializer, DriverSerializer


class DriverListCreateView(generics.ListCreateAPIView):
    """
    GET: List all drivers (with search, filtering, and ordering)
    POST: Create a new driver record
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'phone', 'license_number']
    ordering_fields = ['name', 'created_at', 'status']
    ordering = ['name']


class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single driver profile
    PUT/PATCH: Update driver details or availability status
    DELETE: Remove a driver record
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    lookup_field = 'pk'


class ShipmentListCreateView(generics.ListCreateAPIView):
    """
    GET: List all shipments (with search, filtering, and ordering)
    POST: Create a new shipment
    """
    queryset = Shipment.objects.select_related('driver').all()
    serializer_class = ShipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'driver']
    search_fields = ['tracking_number', 'destination_address', 'destination_city', 'driver__name']
    ordering_fields = ['created_at', 'status', 'tracking_number']
    ordering = ['-created_at']  # Default: newest shipments first


class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single shipment
    PUT/PATCH: Update shipment status or details
    DELETE: Remove a shipment record
    """
    queryset = Shipment.objects.select_related('driver').all()
    serializer_class = ShipmentSerializer
    lookup_field = 'pk'