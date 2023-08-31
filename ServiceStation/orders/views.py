from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OrderForm, OrderAdminForm, CarForm, OrderDateForm
from account.models import Car
from .models import Order, OrderDate
from django.http import HttpResponseRedirect
from account.models import Profile
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 
import datetime
# Create your views here.

@login_required 
def orders(request):
    if request.user.is_superuser:
        object_list = Order.objects.order_by('-created_at')
    else:
        object_list = request.user.orders.all().order_by('-created_at')
    if request.method == 'POST':
        if request.POST.get('search-filter') == 'First name':
            object_list = object_list.filter(user__first_name__contains=request.POST.get('query'))
        elif request.POST.get('search-filter') == 'Second name':
            object_list = object_list.filter(user__last_name__contains=request.POST.get('query'))
        elif request.POST.get('search-filter') == 'Car make':
            object_list = object_list.filter(car__make__contains=request.POST.get('query'))
        elif request.POST.get('search-filter') == 'Car model':
            object_list = object_list.filter(car__model__contains=request.POST.get('query'))
        elif request.POST.get('search-filter') == 'Car vin':
            object_list = object_list.filter(car__vin__contains=request.POST.get('query'))
        elif request.POST.get('search-filter') == 'Type':
            object_list = object_list.filter(type__contains=request.POST.get('query'))
        elif request.POST.get('search-filter') == 'Date':
            object_list = object_list.filter(created_at__contains=request.POST.get('query'))
    filter = request.GET.get('filter')
    filter_values = {'waiting':'Waiting', 'in-progress':'In progress', 'completed':'Completed', 'cancelled':'Cancelled'}
    if filter:
        object_list = object_list.filter(status=filter_values[filter])
    query = request.GET.get('query')
    search = request.GET.get('search')
    if query:
        if search == 'First%name':
            object_list = object_list.filter(user__first_name__contains=query)
        elif search == 'Second%name':
            object_list = object_list.filter(user__last_name__contains=query)
        elif search == 'Car%make':
            object_list = object_list.filter(car__make__contains=query)
        elif search == 'Car%model':
            object_list = object_list.filter(car__model__contains=query)
        elif search == 'Car%vin':
            object_list = object_list.filter(car__vin__contains=query)
        elif search == 'Type':
            object_list = object_list.filter(type__contains=query)
        elif search == 'Date':
            object_list = object_list.filter(created_at__contains=query)
    paginator = Paginator(object_list, 3) # По 3 статьи на каждой странице.    
    page = request.GET.get('page')
    try:        
        orders = paginator.page(page)
        print('Orders:', orders.object_list)   
    except PageNotAnInteger:        # Если страница не является целым числом, возвращаем первую страницу.        
        orders = paginator.page(1)   
        print('PgNotInt:', orders)
    except EmptyPage:        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.        
        orders = paginator.page(paginator.num_pages)  
        print('EmptPg:', orders)
    
    return render(request, 'orders.html', {'section':'orders', 'orders':orders, 'page':page, 'filter':filter, 'search':request.POST.get('search-filter'), 'query':request.POST.get('query')})

@csrf_exempt
@login_required
def appointment(request):
    if request.method == 'POST':
        if request.POST.get('chosing'):
            new_date = OrderDate.objects.filter(date='{}-{}-{}'.format(datetime.datetime.now().year, request.POST['month'], request.POST['day']))
            selected_times = [str(i.time)[:5] for i in new_date]
            times = [i[0] for i in OrderDate.ORDER_DATE_CHOICES]
            print('sel:', selected_times)
            print('tim:', times)
            print(set(times) - set(selected_times))
            return JsonResponse({'status':'ok', 'times':sorted(list(set(times) - set(selected_times)))})
        else:
            order_form = OrderForm(request.POST)
            car_form = CarForm(request.POST)
            date_form = OrderDateForm(request.POST)
            if order_form.is_valid():
                new_order = order_form.save(commit=False)
                new_order.user = request.user
                new_order.profile = Profile.objects.get(id=request.user.id)
                new_order.status = 'Waiting'
                if not request.user.car.count():
                    new_car = car_form.save(commit=False)
                    new_car.user = request.user
                    new_car.save()
                    new_order.car = new_car
                else:
                    new_order.car = Car.objects.get(id=request.POST.get('car-select'))
                new_date = date_form.save(commit=False)
                new_date.order_id = new_order.id
                new_date.time = request.POST.get('time-select')
                new_date.order_id = Order.objects.all().order_by('-created_at')[0].id + 1
                new_date.save()
                new_order.date = new_date
                new_order.save()
            return HttpResponseRedirect('/orders/')
    else:
        date_form = OrderDateForm()
        car_form = CarForm()
        order_form = OrderForm()
        cars = request.user.car.all() 
        times = [i[0] for i in OrderDate.ORDER_DATE_CHOICES]
        return render(request, 'appointment.html', {'section':'appointment', 'order_form':order_form, 'car_form':car_form, 'date_form':date_form,'cars':cars, 'times':times})

@login_required
@staff_member_required
def order_edit(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        prev_status = order.status
        order_form = OrderAdminForm(instance=order, data=request.POST) 
        if order_form.is_valid():
            if prev_status == 'Waiting' and request.POST['status'] == 'In progress':
                car_info = order.car.make + ' ' + order.car.model + ' ' + str(order.car.year) + ' ' + order.car.vin
                subject = 'Your request accepted'
                message = "Your request for {} accepted\
                          \nWe're waiting for you {} at {}\
                          \nType: {}\
                          \nYour message: {}\
                          \nExpected order cost: {}$\
                          \nAll information about your orders is avaliable in your profile: \
                          \n{}" \
                          .format(car_info, order.date.date, str(order.date.time)[:5], order.type, order.message, order.price, request.build_absolute_uri().replace('edit/'+str(order.id), ''))
                #send_mail(subject, message, 'vladimir.gitsarev@gmail.com', [order.user.email])
            elif prev_status == 'In progress' and request.POST['status'] == 'Completed':
                order.closed_at = datetime.datetime.now()
                car_info = order.car.make + ' ' + order.car.model + ' ' + str(order.car.year) + ' ' + order.car.vin
                subject = 'Your order completed'
                message = "Your order for {} completed\
                          \nType: {}\
                          \nYour message: {}\
                          \nOrder cost: {}$\
                          \nAll information about your orders is avaliable in your profile: \
                          \n{}"\
                          .format(car_info, order.type, order.message, order.price, request.build_absolute_uri().replace('edit/'+str(order.id), ''))
                #send_mail(subject, message, 'vladimir.gitsarev@gmail.com', [order.user.email])
            elif prev_status == 'Waiting' and request.POST['status'] == 'Cancelled':
                car_info = order.car.make + ' ' + order.car.model + ' ' + str(order.car.year) + ' ' + order.car.vin
                subject = 'Your order cancelled'
                message = "Your request for {} cancelled\
                          \nType: {}\
                          \nYour message: {}\
                          \nAll information about your orders is avaliable in your profile: \
                          \n{}" \
                          .format(car_info, order.type, order.message, request.build_absolute_uri().replace('edit/'+str(order.id), ''))
                #send_mail(subject, message, 'vladimir.gitsarev@gmail.com', [order.user.email])
            order_form.save()
        return HttpResponseRedirect('/orders/')
    else:   
        order_form = OrderAdminForm(instance=order)
        return render(request, 'order_edit.html', {'section':'order', 'order':order, 'order_form':order_form})

