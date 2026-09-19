from django.urls import path
from .views import (
    DriverListCreateView,
    DriverDetailView,
    ShipmentListCreateView,
    ShipmentDetailView,
)

urlpatterns = [
    # Driver Endpoints
    path('drivers/', DriverListCreateView.as_view(), name='driver-list-create'),
    path('drivers/<int:pk>/', DriverDetailView.as_view(), name='driver-detail'),

    # Shipment Endpoints
    path('shipments/', ShipmentListCreateView.as_view(), name='shipment-list-create'),
    path('shipments/<int:pk>/', ShipmentDetailView.as_view(), name='shipment-detail'),
]