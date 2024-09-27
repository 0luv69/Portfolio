# api/contact_handler.py

import requests
from django.core.mail import send_mail
from django.conf import settings
import json


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
        ip_address = data.get('ip_address', 'Unknown')
        auth_id = data.get('random_num', 'Unknown')
        name = data.get('name', 'Unknown')
        email = data.get('email', 'Unknown')

        # Handle the data securely
        print(f"IP: {ip_address}, Name: {name}, Email: {email}")

        # Send response back
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response_data = {"status": "success", "message": "Contact handler route hit successfully"}
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

    # def do_GET(self):
        # Get query parameters from the URL
        query = self.path.split('?')[-1]  # Extract query string
        params = dict(param.split('=') for param in query.split('&'))

        ip_address = params.get('ip_address', 'Unknown')
        name = params.get('name', 'Unknown')
        email = params.get('email', 'Unknown')

        # Log the request parameters for debugging
        print(f"IP: {ip_address}, Name: {name}, Email: {email}")

        # Prepare the response data
        response_data = {
            "status": "success",
            "message": "Contact handler route hit successfully",
            "ip_address": ip_address,
            "name": name,
            "email": email
        }

        # Send HTTP status code
        self.send_response(200)
        
        # Set headers
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        # Write the response body
        self.wfile.write(json.dumps(response_data).encode("utf-8"))
