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


import json

def handler(request):
    print("Handler function was called successfully!")
    
    # Get query parameters (if needed)
    ip_address = request.GET.get('ip_address', None)
    name = request.GET.get('name', None)
    email = request.GET.get('email', None)

    # You can perform additional processing here
    print(f"IP: {ip_address}, Name: {name}, Email: {email}")

    # Example response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "success",
            "message": "Contact handler route hit successfully"
        })
    }


# def handler(event, context=None):
#     """
#     Vercel-compatible handler function that extracts parameters from the event dictionary.
#     """
#     print("Received event:", event)

#     # Extract parameters if they exist in the event structure
#     try:
#         # If using queryStringParameters (common in AWS Lambda format)
#         ip_address = event.get('queryStringParameters', {}).get('ip_address', 'Unknown IP')
#         name = event.get('queryStringParameters', {}).get('name', 'Unknown Name')
#         email = event.get('queryStringParameters', {}).get('email', 'Unknown Email')

#         # Log the extracted parameters
#         print(f"Extracted IP Address: {ip_address}, Name: {name}, Email: {email}")
        
#         # Respond with extracted parameters
#         response = {
#             "statusCode": 200,
#             "body": json.dumps({
#                 "status": "success",
#                 "message": "Handler executed successfully!",
#                 "ip_address": ip_address,
#                 "name": name,
#                 "email": email
#             })
#         }
#     except Exception as e:
#         print(f"Error extracting parameters: {e}")
#         response = {
#             "statusCode": 500,
#             "body": json.dumps({
#                 "status": "error",
#                 "message": f"Failed to extract parameters: {str(e)}"
#             })
#         }

#     return response

