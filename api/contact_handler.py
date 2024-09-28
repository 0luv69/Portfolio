# api/contact_handler.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protfolio.settings')
django.setup()  # Initialize Django

from django.conf import settings
from main.models import *  # Import your models


import requests
from http.server import BaseHTTPRequestHandler
import json


from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string



# Function to create IP info object
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

# Function to fetch IP info
def fetch_ip_info(ip_address, api_service="ipapi.co", can_switch=True):
    url = f"https://{api_service}/{ip_address}/json"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.json()
        elif can_switch:
            return fetch_ip_info(ip_address, "ipinfo.io", False)
    except requests.RequestException as e:
        print(f"Error fetching IP info: {e}")
        return None


def send_email(name, email, topic):
    subject = "Thank You for Contacting Us"
    email_from = settings.EMAIL_HOST_USER
    to = [email]

    # Context for rendering the HTML template
    context = {
        'name': name,
        'topic': topic,
        'logo_url': 'https://www.rujalbaniya.com.np/staticfiles/img/logo.png',  
    }
    # Render the HTML content using a template for better manageability
    html_content = render_to_string('emails/contact_response.html', context)


    # Plain text version (fallback)
    text_content = f'''
    Hi {name},


    Thank you for reaching out to us.   We have received your message and will get back to you shortly.

    We will have a great talk on {topic}.




    *note*: This is an automated message. Please do wait I value your Time and Effort.


    You can also reach me at
    Email: baniyarujal@gmail.com

    Github: https://www.github.com/0luv69
    linkedin: https://www.linkedin.com/in/luv-79a89732a/


    Best regards,
    Rujal Baniya `aka Luv`

    '''

    
    
    msg = EmailMultiAlternatives(subject, text_content, email_from, to)
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send()
    except Exception as e:
        print(f"Error sending email: {e}")
    

class handler(BaseHTTPRequestHandler):
   def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response_data = {"status": "sucess", "message": "This Rujal Baniya's Site, A passionate Full Stack Developer from Nepal, specializing in Python, cybersecurity, and web development. Have done project in tkinter, Django, won Hackathon, Ideathon also specialized on cybersecurity and more. Got once reconized by Nepal Government for my work. Here you can find my projects where I have worked on such as Photo editor, Student Health based Pariwar Application, Student Learning based Mcqchamps to learn tick and test mcq with ppt posting project in-build."}
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

   def do_POST(self):
        try:
            # Read the content length to know how much data to read
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Read the request body
            data = json.loads(post_data)
            
            # Parse POST data (assuming it's JSON)
            ip_address = data.get('ip_address', None)
            name = data.get('name', None)
            email = data.get('email', None)

            auth_id = data.get('random_num', None)
            obj_id = data.get('obj_id', None)

            try:
                contact = Contact.objects.get(id=obj_id)
            except Contact.DoesNotExist:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "Invalid contact ID"}).encode("utf-8"))
                return
            
            # Authenticate using random_num (auth_uuid)
            if str(contact.auth_uuid) == auth_id:
                # Fetch IP information
                ip_info_data = fetch_ip_info(ip_address)
                if not ip_info_data:
                    print("Failed to fetch IP information.")

                # Create IP info object and link to contact
                INFO_OBJ = create_IP_INFO_obj(ip_info_data, contact)

                # Send an email in the background
                send_email(name, email, contact.subject)
            else:
                print("Authentication is wrong, Invalid random_num provided.")

            # Send response back
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response_data = {"status": "success", "message": "Contact handler route hit successfully"}
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "No post request plz only get"}).encode("utf-8"))

