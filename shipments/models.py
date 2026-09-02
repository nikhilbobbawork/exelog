from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=50, unique=True)
    destination = models.TextField()
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)