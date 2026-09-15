from django.urls import path
from .views import ShipmentListCreateView, ShipmentDetailView

urlpatterns = [
    path('', ShipmentListCreateView.as_view(), name='shipment-list-create'),
    path('<int:pk>/', ShipmentDetailView.as_view(), name='shipment-detail'),
]