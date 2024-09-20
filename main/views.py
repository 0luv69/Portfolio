from django.shortcuts import render, redirect
from .models import *
import requests
from requests.exceptions import RequestException

# Create your views here.
# importing setting to check its value 

def home(request):

    return render(request, 'pages/index.html', {})

def test(request):
    return render(request, 'pages/test.html', {})

def t2(request):
    return render(request, 'pages/t2.html', {})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def fetch_ip_info(ip_address):
    url = f"https://ipapi.co/{ip_address}/json"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.json()
    except RequestException as e:...
    return None

def create_IP_INFO_obj(ip_info_data):
    if ip_info_data:
        # Save the IP information
        ip_info = IPAddressInfo.objects.create(
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


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        Subject = request.POST['subject']

        message = request.POST['message']   
        ip_address = get_client_ip(request)
        ip_info_data = fetch_ip_info(ip_address)
        print(ip_info_data)


        INFO_OBJ = create_IP_INFO_obj(ip_info_data)
        contact = Contact(name=name, email=email, subject= Subject, message=message, ip_address = ip_address, ip_address_info = INFO_OBJ)
        contact.save()
    
    return redirect('home')
