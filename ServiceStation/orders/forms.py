from django import forms
from django.contrib.auth.models import User
from django.forms import Select
from .models import Order, OrderDate
from account.models import Car
from django.forms import SelectDateWidget
from datetime import datetime

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('make', 'model', 'year', 'vin')
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('type', 'message')
        labels = {
            'type': ('Укажите тип поддержки')
        }
        help_texts = {
            'message': ('Сообщение')
        } 

class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('type', 'status', 'price')

class OrderDateForm(forms.ModelForm):
    class Meta:
        model = OrderDate
        fields = ('date', )
        widgets = {
            'date': SelectDateWidget(years=set([datetime.now().year])),
        }