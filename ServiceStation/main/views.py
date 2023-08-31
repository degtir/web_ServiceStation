from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'main.html', {'section':'main'})

def services(request):
    return render(request, 'services.html', {'section':'services'})