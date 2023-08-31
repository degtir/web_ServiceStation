from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    date_of_birth = models.DateField(blank=True, null=True)    
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=100)

    def __str__(self):        
        return 'Profile for user {}'.format(self.user.username) 

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=10)
