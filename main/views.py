import random

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



# Create your views here.

video_list = [
    "vid/fire1.mp4",
    "vid/love-anger.mp4",
    "vid/love.mp4"
]

def home(request):
    final_list= []
    for i in range(5,0,-1):
        particular_grp= Project.objects.filter(sort_order=i).order_by('?')
        final_list.extend(list(particular_grp))
    projects = final_list
    technologies = Technology.objects.all().order_by('-order')
    selected_video_index = random.randint(0, len(video_list) - 1)
    selected_video_url = video_list[selected_video_index]
    print("selected_video_url", selected_video_url, "selected_video_index", selected_video_index)
    return render(request, 'pages/index.html', {'projects':projects, 'technologies': technologies, 'video_list': video_list, 'selected_video_url':  selected_video_url , 'selected_video_index':  selected_video_index})


def project_detail(request, slug):
    project = Project.objects.filter(slug=slug).first()
    if not project:
        return HttpResponse("Project not found, Sorry!", status=404)
    return render(request, 'pages/project_detail.html', {'project': project})


def old_portfolio(request):
    final_list= []
    for i in range(5,0,-1):
        particular_grp= Project.objects.filter(sort_order=i).order_by('?')
        final_list.extend(list(particular_grp))
    projects = final_list
    return render(request, 'pages/old.html', {'projects':projects})


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




from django.http import JsonResponse
from .models import Project


def project_list_json(request):
    projects = Project.objects.all().order_by("-created_at")

    data = []

    for p in projects:
        data.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "image": p.image.url if p.image else None,
            "btn1_text": p.btn1_text,
            "btn1_url": p.btn1_url,
            "btn2_text": p.btn2_text,
            "btn2_url": p.btn2_url,
            "sort_order": p.sort_order,
            "created_at": p.created_at,
        })

    return JsonResponse({
        "status": "ok",
        "count": len(data),
        "projects": data
    })