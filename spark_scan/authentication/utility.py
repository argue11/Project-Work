import random
import string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from twilio.rest import Client
from decouple import config


def password_generator():
    """Generate random 8-character password"""
    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    return password


def sending_email(subject, template, context, recipient):
    """Send email using Django email backend"""
    sender = settings.EMAIL_HOST_USER
    email_obj = EmailMultiAlternatives(subject, from_email=sender, to=[recipient])
    content = render_to_string(template, context)
    email_obj.attach_alternative(content, "text/html")
    email_obj.send()


def generate_otp(length=6):
    """Generate OTP of specified length (default 6 digits)"""
    otp = "".join(random.choices(string.digits, k=length))
    return otp


def send_phone_sms(phone_num, otp, message_template=None):
    """
    Send OTP via Twilio SMS
    
    Args:
        phone_num: Phone number with country code (e.g., +917559942623)
        otp: The OTP to send
        message_template: Optional custom message. If None, uses default.
    """
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    from_num = config("TWILIO_FROM_NUMBER")
    
    client = Client(account_sid, auth_token)
    
    if message_template:
        body = message_template.format(otp=otp)
    else:
        body = f"Your OTP for verification is: {otp}\n\nValid for 10 minutes.\n- KSEB Customer Care"
    
    message = client.messages.create(
        from_=from_num,
        to=phone_num,
        body=body
    )
    
    return message.sid


def send_whatsapp_message(phone_num, message_body):
    """
    Send WhatsApp message via Twilio
    
    Args:
        phone_num: Phone number with country code (e.g., +917559942623)
        message_body: Message content to send
    """
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    from_whatsapp = config("TWILIO_WHATSAPP_NUMBER")  # e.g., +14155238886
    
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        from_=f'whatsapp:{from_whatsapp}',
        to=f'whatsapp:{phone_num}',
        body=message_body
    )
    
    return message.sid


def send_complaint_confirmation_whatsapp(phone_num, complaint_id, asset_number, tracking_url):
    """
    Send WhatsApp confirmation for complaint registration
    
    Args:
        phone_num: Reporter's phone number
        complaint_id: Generated complaint ID (e.g., CPN-2024-0012)
        asset_number: Asset number (e.g., POLE-001)
        tracking_url: URL to track complaint status
    """
    message_body = f"""✅ *Complaint Registered Successfully!*

📋 Complaint ID: *{complaint_id}*
🔌 Asset: *{asset_number}*
📊 Status: *Submitted*

Track your complaint:
{tracking_url}

We will inspect and resolve this issue soon.

- KSEB Customer Care Team"""
    
    return send_whatsapp_message(phone_num, message_body)


def send_status_update_whatsapp(phone_num, complaint_id, new_status):
    """
    Send WhatsApp notification for complaint status updates
    
    Args:
        phone_num: Reporter's phone number
        complaint_id: Complaint ID
        new_status: New status (INSPECTING, REPAIRING, COMPLETED)
    """
    status_messages = {
        'INSPECTING': '🔍 Your complaint is now under inspection.',
        'REPAIRING': '🔧 Repair work has started.',
        'COMPLETED': '✅ Your complaint has been resolved!'
    }
    
    message_body = f"""📢 *Status Update*

Complaint ID: *{complaint_id}*
New Status: *{new_status}*

{status_messages.get(new_status, 'Status updated.')}

- KSEB Customer Care"""
    
    return send_whatsapp_message(phone_num, message_body)