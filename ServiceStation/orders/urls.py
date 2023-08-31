from django.urls import path, include
from . import views

urlpatterns = [     
    path('', views.orders, name='orders'), 
    path('appointment', views.appointment, name='appointment'),
    path('edit/<int:order_id>', views.order_edit, name='order_edit')
] 