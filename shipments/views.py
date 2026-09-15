from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Shipment
from .serializers import ShipmentSerializer


class ShipmentListCreateView(generics.ListCreateAPIView):
    """
    GET: List all shipments (with search, filtering, and ordering)
    POST: Create a new shipment
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['tracking_number', 'destination', 'driver_name']
    ordering_fields = ['created_at', 'status', 'tracking_number']
    ordering = ['-created_at']  # Default: newest shipments first


class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single shipment
    PUT/PATCH: Update shipment status or details
    DELETE: Remove a shipment record
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    lookup_field = 'pk'