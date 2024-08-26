from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    return render(request, 'pages/index.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        contact = Contact(name=name, email=email, message=message)
        contact.save()
    
    return render(request, 'pages/index.html')
