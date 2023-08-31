from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from account.models import Car, Profile

# Create your models here.

class OrderDate(models.Model):
    ORDER_DATE_CHOICES = [
        ('09:00', '09:00:00'),
        ('10:00', '10:00:00'),
        ('11:00', '11:00:00'),
        ('12:00', '12:00:00'),
        ('13:00', '13:00:00'),
        ('14:00', '14:00:00'),
        ('15:00', '15:00:00'),
        ('16:00', '16:00:00')
    ]
    order_id = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()

class Order(models.Model):
    WORK_TYPE_CHOICES = [
        ('Live support','Live support'),
        ('Repair service', 'Repair service'),
        ('Complete care', 'Complete care'),
        ('Spare parts', 'Spare parts'),
        ('Sales service', 'Sales service'),
        ('Tyre service', 'Tyre service'),
        ('Other', 'Other')
    ]
    STATUS_CHOICES = (
        ('Waiting', 'Waiting'),
        ('In progress', 'In progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_orders')
    date = models.ForeignKey(OrderDate, on_delete=models.CASCADE, default=1, related_name='order_dates')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='cars')
    type = models.CharField(choices=WORK_TYPE_CHOICES, max_length=50, default='Other') 
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Waiting')
    price = models.FloatField(null=True)
    message = models.TextField(max_length=250)

