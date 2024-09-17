from django.shortcuts import render, redirect
from .models import *

# Create your views here.
# importing setting to check its value 

def home(request):

    return render(request, 'pages/index.html', {})



def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        Subject = request.POST['subject']

        message = request.POST['message']

        contact = Contact(name=name, email=email, subject= Subject, message=message)
        contact.save()
    
    return redirect('home')
