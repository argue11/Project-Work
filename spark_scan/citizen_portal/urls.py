# citizen_portal/urls.py
from django.urls import path
from . import views

app_name = 'citizen_portal'

urlpatterns = [
    # Complaint Form - When user scans QR code
    path('report/<str:asset_id>/', 
         views.ComplaintFormView.as_view(), 
         name='complaint_form'),
    
    # OTP Verification
    path('verify-otp/<uuid:complaint_id>/', 
         views.VerifyOTPView.as_view(), 
         name='verify_otp'),
    
    # Resend OTP
    path('resend-otp/<uuid:complaint_id>/', 
         views.ResendOTPView.as_view(), 
         name='resend_otp'),
    
    # Success Page
    path('complaint-success/', 
         views.ComplaintSuccessView.as_view(), 
         name='complaint_success'),
    
    # Check Complaint Status
    path('complaint-status/<uuid:complaint_id>/', 
         views.ComplaintStatusView.as_view(), 
         name='complaint_status'),

    path('qr/<str:asset_number>/', views.generate_pole_qr, name='generate_qr'),
]