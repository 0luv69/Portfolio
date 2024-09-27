# api/contact_handler.py

import requests
from django.core.mail import send_mail
from django.conf import settings
import json


from main.models import *


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


def fetch_ip_info(ip_address, api_service="ipapi.co", can_switch=True):
    url = f"https://{api_service}/{ip_address}/json"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.json()
        elif can_switch:
            return fetch_ip_info(ip_address, "ipinfo.io", False)
    except requests.RequestException:
        return None


def send_email(name, email):
    subject = f"Regarding the Talk"
    email_body = f'''
        Hi {name},

        Thank you for reaching out. We have received your message and will get back to you soon.

        Regards,
        Rujal Baniya
    '''
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, email_body, email_from, [email])


# def handler(request):
#     # Extract parameters from request
#     ip_address = request.GET.get('ip_address')
#     name = request.GET.get('name')
#     email = request.GET.get('email')

#     # Fetch IP information
#     ip_info_data = fetch_ip_info(ip_address)

#     # Send an email in the background
#     send_email(name, email)

#     return {"status": "success", "ip_info": ip_info_data}

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

   def do_POST(self):
        # Read the content length to know how much data to read
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  # Read the request body
        
        # Parse POST data (assuming it's JSON)
        data = json.loads(post_data)
        ip_address = data.get('ip_address', None)
        name = data.get('name', None)
        email = data.get('email', None)

        auth_id = data.get('random_num', None)
        obj_id = data.get('quenum', None)

        contact = Contact.objects.get(id=obj_id)
        if contact.random_num == auth_id:
            # Fetch IP information
            ip_info_data = fetch_ip_info(ip_address)

            INFO_OBJ = create_IP_INFO_obj(ip_info_data, contact)

            # Send an email in the background
            send_email(name, email)
        else:
            print("Authentication is wrong")

        # Send response back
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response_data = {"status": "success", "message": "Contact handler route hit successfully"}
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

