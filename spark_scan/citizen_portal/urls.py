from django.urls import path
from . import views

app_name = 'citizen_portal'

urlpatterns = [
    # Step 1: Phone Number Entry (QR Code lands here)
    path('report/<int:asset_id>/', views.ReportComplaintStep1View.as_view(), name='report_step1'),
    
    # Step 2: OTP Verification
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    
    # Step 3: Complaint Form
    path('submit-complaint/', views.SubmitComplaintView.as_view(), name='submit_complaint'),
    
    # Success Page
    path('success/<str:complaint_id>/', views.ComplaintSuccessView.as_view(), name='complaint_success'),
    
    # Public Tracking
    path('track/<str:complaint_id>/', views.TrackComplaintView.as_view(), name='track_complaint'),
]