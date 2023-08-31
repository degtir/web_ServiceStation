from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [    
    path('', views.main, name='main'), 
    path('services/', views.services, name='services'),
] 