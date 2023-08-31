from django.http import HttpResponse 
from django.shortcuts import render 
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.db import models 
from django.conf import settings
from .models import Profile, Car
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, CarForm
from django.http import JsonResponse 
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect


@login_required 
@csrf_exempt
def profile(request):   
    profile = Profile.objects.get(id=request.user.id)
    cars = request.user.car.all() 
    if request.method == 'POST':
        car = Car(
            user_id = request.user.id, 
            make = request.POST.get('make'),
            model = request.POST.get('model'),
            year = request.POST.get('year'),
            vin = request.POST.get('vin')
            )
        car.save()
        car_json = {'id':car.id, 'make':car.make, 'model':car.model, 'year':car.year, 'vin':car.vin}
        return JsonResponse({'status':'ok', 'car':car_json})
    else:
        car_form = CarForm()
    return render(request,'account/profile.html',{'section': 'profile', 'profile': profile, 'cars':cars, 'car_form':car_form}) 

@login_required 
def edit(request):
    if request.method == 'POST':        
        user_form = UserEditForm(instance=request.user,data=request.POST)        
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)        
        if user_form.is_valid() and profile_form.is_valid():            
            user_form.save()            
            profile_form.save()   
        return HttpResponseRedirect('/account/') 
    else:        
        user_form = UserEditForm(instance=request.user)        
        profile_form = ProfileEditForm(instance=request.user.profile)   
        return render(request,'account/edit.html', {'user_form': user_form,'profile_form': profile_form}) 
    

def register(request):    
    if request.method == 'POST':        
        user_form = UserRegistrationForm(request.POST)     
        profile_form = ProfileEditForm(request.POST)   
        if user_form.is_valid() and profile_form.is_valid():                    
            new_user = user_form.save(commit=False)                        
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()   
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save() 
            return render(request, 'account/register_done.html', {'new_user': new_user})    
    else:        
        user_form = UserRegistrationForm() 
        profile_form = ProfileEditForm()   
    return render(request,'account/register.html',{'user_form': user_form, 'profile_form':profile_form})

@login_required 
@csrf_exempt
def delete_car(request):
    try:
        car_id = request.POST.get('id') 
        car = Car.objects.get(id=car_id)
        if car.user_id == request.user.id:
            if request.user.orders.filter(car_id=car_id).count():
                return JsonResponse({'status':'error'})
            else:
                car.delete()
        else:
            car = None
    except:
        car = None
    return JsonResponse({'status':'ok'}) 