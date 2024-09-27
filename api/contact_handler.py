# api/contact_handler.py

import requests
from django.core.mail import send_mail
from django.conf import settings

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

def handler(request):
    # Extract parameters from request
    ip_address = request.GET.get('ip_address')
    name = request.GET.get('name')
    email = request.GET.get('email')

    # Fetch IP information
    ip_info_data = fetch_ip_info(ip_address)

    # Send an email in the background
    send_email(name, email)

    return {"status": "success", "ip_info": ip_info_data}
