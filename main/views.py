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

def home(request):
    final_list= []
    for i in range(5,0,-1):
        particular_grp= Project.objects.filter(prj_value=i).order_by('?')
        final_list.extend(list(particular_grp))
    projects = final_list
    return render(request, 'pages/index.html', {'projects':projects})

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
    return render(request, 'others/another.html', {})

def test(request):
    return render(request, 'others/test.html', {})

# main/views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Project

@csrf_exempt
def import_projects_json(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed.'}, status=405)

    try:
        body = request.body.decode('utf-8')
        try:
            # First, try the simple case: a single JSON array
            data = json.loads(body)
            if not isinstance(data, list):
                raise ValueError("Expected a list of project entries.")
        except ValueError as ve:
            # Fallback: parse multiple JSON values concatenated together
            decoder = json.JSONDecoder()
            pos = 0
            length = len(body)
            data = []
            while pos < length:
                obj, idx = decoder.raw_decode(body, pos)
                pos = idx
                # if it's a list, extend; otherwise, append single object
                if isinstance(obj, list):
                    data.extend(obj)
                else:
                    data.append(obj)
                # skip any whitespace/newlines between JSON values
                while pos < length and body[pos] in ' \r\n\t':
                    pos += 1

        # Now `data` is a flat list of project dicts
        for item in data:
            fields = item['fields']
            project, created = Project.objects.update_or_create(
                pk=item['pk'],
                defaults={
                    'title':       fields['title'],
                    'description': fields['description'],
                    'btn1_text':   fields['btn1_text'],
                    'btn1_url':    fields['btn1_url'],
                    'btn2_text':   fields['btn2_text'],
                    'btn2_url':    fields['btn2_url'],
                    'prj_value':   fields['prj_value'],
                    'created_at':  parse_datetime(fields['created_at']),
                }
            )
            # If an image path was provided, assign it directly
            if fields.get('image'):
                project.image.name = fields['image']
                project.save()

        return JsonResponse({'status': 'success', 'message': 'Projects imported successfully.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)