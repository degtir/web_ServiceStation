from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [    # Обработчики действий со статьями.    
    # path('login/', auth_views.LoginView.as_view(), name='login'),   
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.profile, name='profile'), 
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'), 
    path('delete_car/', views.delete_car, name='delete_car'),
] 