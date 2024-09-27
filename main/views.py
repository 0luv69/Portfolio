from django.shortcuts import render, redirect
from .models import *
import requests
from requests.exceptions import RequestException

from django.conf import settings
from django.core.mail import send_mail
import time
import uuid

# Create your views here.
# importing setting to check its value 

def home(request):

    return render(request, 'pages/index.html', {})

def seo(request):
    return render(request, 'pages/seo.html', {})

def t2(request):
    return render(request, 'pages/t2.html', {})

def test(request):
    return render(request, 'pages/test.html', {})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def fetch_ip_info(ip_address, api_service ="ipapi.co", Can_Switch= True ):
    url = f"https://{api_service}/{ip_address}/json"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            print("sifting the url to ipinfo.io from ipapi")
            if Can_Switch:
                return fetch_ip_info(ip_address, "ipinfo.io", False)
            else:
                return None
    except RequestException as e:
        print("Time out ......................... to get ip")
        ...
    return None

def create_IP_INFO_obj(ip_info_data, contact):
    if ip_info_data:
        # Save the IP information
        ip_info = IPAddressInfo.objects.create(
            contact=contact,
            ip=ip_info_data.get("ip"),
            network=ip_info_data.get("network"),
            city=ip_info_data.get("city"),
            region=ip_info_data.get("region"),
            region_code=ip_info_data.get("region_code"),
            country_name=ip_info_data.get("country_name"),
            country_code=ip_info_data.get("country_code"),
            continent_code=ip_info_data.get("continent_code"),
            latitude=ip_info_data.get("latitude"),
            longitude=ip_info_data.get("longitude"),
            timezone=ip_info_data.get("timezone"),
            utc_offset=ip_info_data.get("utc_offset"),
            org=ip_info_data.get("org"),
            asn=ip_info_data.get("asn"),
            currency=ip_info_data.get("currency"),
            languages=ip_info_data.get("languages"),
        )
    else:
        ip_info = None
    
    return ip_info


def email_sending(email, datas):
    # Construct the subject and message
    subject = datas['subject']
    email_from = settings.EMAIL_HOST_USER

        # Create the email message
    message = f'''
        Hi, {datas['name']}

        Email from: {email}
        We received a Email from you thanks, we would loved to further have convercation, let admin get live to reply.


        If you did not request a password reset, please ignore this email.

        Thanks,
        Rujal Baniya
        For Your Security, Please Do Not Forward This Email, or Share This Link With Anyone.
        '''
    send_mail(subject, message, email_from, [email])


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
        vercel_url = 'https://www.rujalbaniya.com.np/contact-handler'
        try:
            requests.post(vercel_url, json=params, timeout=1)
        except requests.RequestException:
            pass  # Ignore any issues with background task
    
    return redirect('home')

        # ip_info_data = fetch_ip_info(ip_address)
        # INFO_OBJ = create_IP_INFO_obj(ip_info_data, contact)
        # datas = {
        #     'name': name,
        #     'subject': "Regarding the Talk"
        # }
        # # email_sending(email, datas)

def contact_messages_view(request):
    # Fetch all contact messages from the database
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'admin/custom_messages.html', {'contacts': contacts})

