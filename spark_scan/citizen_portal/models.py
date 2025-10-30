# citizen_portal/models.py
from django.db import models
import uuid
import random
from django.utils import timezone
from datetime import timedelta
from asset.models import Pole  # ← IMPORT YOUR POLE MODEL

# ▼▼▼ REMOVE the Pole model from here - we're using yours from asset app ▼▼▼
# DELETE this entire Pole class if you have it:
# class Pole(models.Model):
#     ... etc ...

# KEEP ONLY Complaint and ComplaintImage models:
class Complaint(models.Model):
    SAFETY_HAZARDS = [
        ('LEANING_POLE', 'Leaning Pole'),
        ('EXPOSED_WIRES', 'Exposed Wires'),
        ('SPARKING', 'Sparking'),
        ('CRACKED_POLE', 'Cracked Pole'),
        ('MISSING_COMPONENTS', 'Missing Components'),
        ('VEGETATION_GROWTH', 'Vegetation Growth'),
        ('OTHER', 'Other'),
    ]
    
    COMPLAINT_STATUS = [
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
        ('ASSIGNED', 'Assigned to Technician'),
        ('IN_PROGRESS', 'Repair in Progress'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]
    
    # Complaint Details
    complaint_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    # CHANGE: Link to YOUR Pole model from asset app
    pole = models.ForeignKey(Pole, on_delete=models.CASCADE, related_name='complaints')  # ← THIS LINKS TO YOUR POLE
    safety_hazard = models.CharField(max_length=50, choices=SAFETY_HAZARDS)
    description = models.TextField()
    
    # Contact Information
    mobile_number = models.CharField(max_length=15)
    
    # OTP Verification Fields
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_attempts = models.IntegerField(default=0)
    
    # Status Tracking
    status = models.CharField(max_length=20, choices=COMPLAINT_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.otp_attempts = 0
        self.save()
        print(f"🔐 OTP for {self.mobile_number}: {self.otp}")
        return self.otp
    
    def is_otp_expired(self):
        if not self.otp_created_at:
            return True
        return timezone.now() > self.otp_created_at + timedelta(minutes=10)
    
    def verify_otp(self, entered_otp):
        if self.is_otp_expired():
            return False, "OTP has expired. Please request a new one."
        if self.otp_attempts >= 3:
            return False, "Too many failed attempts. Please request a new OTP."
        if self.otp == entered_otp:
            self.otp_verified = True
            self.otp_attempts = 0
            self.save()
            return True, "OTP verified successfully!"
        else:
            self.otp_attempts += 1
            self.save()
            attempts_left = 3 - self.otp_attempts
            return False, f"Invalid OTP. {attempts_left} attempts left."
    
    def __str__(self):
        return f"Complaint {self.complaint_id} - {self.pole.asset_number}"  # ← CHANGE: asset_number

class ComplaintImage(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='complaint_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.complaint.complaint_id}"