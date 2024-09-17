from django.shortcuts import render, redirect
from .models import *

# Create your views here.
# importing setting to check its value 
from protfolio.settings import PRODUCTION_ENV,USE_SQLITE, DEBUG

def home(request):
    context = { 
        "production": str(PRODUCTION_ENV),
        "sqlite": str(USE_SQLITE),
        "debug": str(DEBUG)

    }
    return render(request, 'pages/index.html', context)



def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        Subject = request.POST['subject']

        message = request.POST['message']

        contact = Contact(name=name, email=email, subject= Subject, message=message)
        contact.save()
    
    return redirect('home')
