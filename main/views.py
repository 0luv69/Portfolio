from django.shortcuts import render, redirect
from .models import *
import requests
from requests.exceptions import RequestException
from django.http import HttpResponse

from django.conf import settings
from django.core.mail import send_mail
import time
import uuid

from django.contrib import messages
from django.db.models.functions import Random


# Create your views here.

def home(request):
    projects = []
    projects = Project.objects.order_by('-prj_value')
    return render(request, 'pages/index.html', {'projects': projects})

def seo(request):
    return render(request, 'pages/seo.html', {})

def contact_messages_view(request):
    # only allow admin user to get the contact message
    print(request.user.is_superuser)
    if request.user.is_superuser:
        return redirect('home')

    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'admin/custom_messages.html', {'contacts': contacts})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        Subject = request.POST['subject'] 

        message = request.POST['message']   
        ip_address = get_client_ip(request)

        auth_uuid = uuid.uuid4()

        contact = Contact(name=name, email=email, subject= Subject, message=message, ip_address = ip_address
                          , auth_uuid = auth_uuid)
        contact.save()

         # Trigger the Vercel background function
        params = {
            'ip_address': ip_address,
            'name': name,
            'email': email,
            'random_num': str(contact.auth_uuid),  # UUID converted to string
            'obj_id': str(contact.id), # Contact ID converted to string
        }
        # Send the request to Vercel's background function endpoint
        vercel_url = 'https://www.rujalbaniya.com.np/whois'
        try:
            requests.post(vercel_url, json=params, timeout=1)
        except requests.RequestException:
            pass  # Ignore any issues with background task
        messages.success(request, 'Your message has been sent successfully. We will contact you soon.')
    return redirect('home')


def handle_loaderio(request):
    return HttpResponse("loaderio-e8dcc5c185655d3febcd86432c9d324e", content_type="text/plain")


def second_one(request):
    projects = Project.objects.order_by('-prj_value')

    return render(request, 'others/another.html', {'projects': projects})

def test(request):
    return render(request, 'others/test.html', {})