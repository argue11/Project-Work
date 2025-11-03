from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
import threading

from .models import Complaint
from .forms import PhoneNumberForm, OTPVerificationForm, ComplaintForm
from asset.models import Asset
from authentication.models import OTP
from authentication.utility import generate_otp, send_phone_sms, send_complaint_confirmation_whatsapp


class ReportComplaintStep1View(View):
    """Step 1: Enter Phone Number (QR Code redirects here)"""
    template_name = 'citizen_portal/step1_phone.html'
    form_class = PhoneNumberForm
    
    def get(self, request, asset_id):
        asset = get_object_or_404(Asset, id=asset_id, status='COMMISSIONED')
        form = self.form_class()
        
        context = {
            'form': form,
            'asset': asset
        }
        return render(request, self.template_name, context)
    
    def post(self, request, asset_id):
        asset = get_object_or_404(Asset, id=asset_id, status='COMMISSIONED')
        form = self.form_class(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            # Generate OTP
            otp_code = generate_otp(6)
            
            # Delete old OTPs for this phone
            OTP.objects.filter(phone_number=phone_number).delete()
            
            # Create new OTP
            OTP.objects.create(
                phone_number=phone_number,
                phone_otp=otp_code,
                verified=False
            )
            
            # Send OTP via SMS (in background)
            thread = threading.Thread(target=send_phone_sms, args=(phone_number, otp_code))
            thread.start()
            
            # Store in session
            request.session['complaint_phone'] = phone_number
            request.session['complaint_asset_id'] = asset_id
            request.session['otp_sent_time'] = timezone.now().timestamp()
            
            messages.success(request, f'OTP sent to {phone_number}')
            return redirect('citizen_portal:verify_otp')
        
        context = {
            'form': form,
            'asset': asset
        }
        return render(request, self.template_name, context)


class VerifyOTPView(View):
    """Step 2: Verify OTP"""
    template_name = 'citizen_portal/step2_verify_otp.html'
    form_class = OTPVerificationForm
    
    def get(self, request):
        phone_number = request.session.get('complaint_phone')
        
        if not phone_number:
            messages.error(request, 'Session expired. Please start again.')
            return redirect('citizen_portal:report_step1')
        
        form = self.form_class()
        otp_sent_time = request.session.get('otp_sent_time')
        remaining_time = 600  # 10 minutes
        
        if otp_sent_time:
            elapsed = timezone.now().timestamp() - otp_sent_time
            remaining_time = max(0, 600 - int(elapsed))
            
            if remaining_time == 0:
                messages.error(request, 'OTP expired. Please request a new one.')
                return redirect('citizen_portal:report_step1')
        
        context = {
            'form': form,
            'phone_number': phone_number,
            'remaining_time': remaining_time
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        phone_number = request.session.get('complaint_phone')
        form = self.form_class(request.POST)
        
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            
            try:
                otp_record = OTP.objects.get(phone_number=phone_number, phone_otp=entered_otp)
                
                if otp_record.is_expired():
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return redirect('citizen_portal:report_step1')
                
                # Mark as verified
                otp_record.verified = True
                otp_record.save()
                
                request.session['otp_verified'] = True
                
                # Proceed to complaint form
                return redirect('citizen_portal:submit_complaint')
                
            except OTP.DoesNotExist:
                messages.error(request, 'Invalid OTP. Please try again.')
        
        otp_sent_time = request.session.get('otp_sent_time')
        remaining_time = 600
        if otp_sent_time:
            elapsed = timezone.now().timestamp() - otp_sent_time
            remaining_time = max(0, 600 - int(elapsed))
        
        context = {
            'form': form,
            'phone_number': phone_number,
            'remaining_time': remaining_time
        }
        return render(request, self.template_name, context)


class SubmitComplaintView(View):
    """Step 3: Submit Complaint Form"""
    template_name = 'citizen_portal/step3_complaint.html'
    form_class = ComplaintForm
    
    def get(self, request):
        phone_number = request.session.get('complaint_phone')
        asset_id = request.session.get('complaint_asset_id')
        otp_verified = request.session.get('otp_verified')
        
        if not phone_number or not asset_id:
            messages.error(request, 'Session expired. Please start again.')
            return redirect('citizen_portal:report_step1')
        
        if not otp_verified:
            messages.error(request, 'Please verify OTP first.')
            return redirect('citizen_portal:verify_otp')
        
        asset = get_object_or_404(Asset, id=asset_id)
        form = self.form_class()
        
        context = {
            'form': form,
            'asset': asset,
            'phone_number': phone_number
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        phone_number = request.session.get('complaint_phone')
        asset_id = request.session.get('complaint_asset_id')
        asset = get_object_or_404(Asset, id=asset_id)
        
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.asset = asset
            complaint.reporter_phone = phone_number
            complaint.save()
            
            # Generate tracking URL
            tracking_url = request.build_absolute_uri(
                reverse('citizen_portal:track_complaint', args=[complaint.complaint_id])
            )
            
            # Send WhatsApp confirmation (in background)
            thread = threading.Thread(
                target=send_complaint_confirmation_whatsapp,
                args=(phone_number, complaint.complaint_id, asset.asset_number, tracking_url)
            )
            thread.start()
            
            # Clear session
            request.session.pop('complaint_phone', None)
            request.session.pop('complaint_asset_id', None)
            request.session.pop('otp_verified', None)
            request.session.pop('otp_sent_time', None)
            
            return redirect('citizen_portal:complaint_success', complaint_id=complaint.complaint_id)
        
        context = {
            'form': form,
            'asset': asset,
            'phone_number': phone_number
        }
        return render(request, self.template_name, context)


class ComplaintSuccessView(View):
    """Success page after complaint submission"""
    template_name = 'citizen_portal/complaint_success.html'
    
    def get(self, request, complaint_id):
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        
        tracking_url = request.build_absolute_uri(
            reverse('citizen_portal:track_complaint', args=[complaint.complaint_id])
        )
        
        context = {
            'complaint': complaint,
            'tracking_url': tracking_url
        }
        return render(request, self.template_name, context)


class TrackComplaintView(View):
    """Public complaint tracking page"""
    template_name = 'citizen_portal/track_complaint.html'
    
    def get(self, request, complaint_id):
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        
        # Calculate progress percentage
        status_progress = {
            'SUBMITTED': 25,
            'INSPECTING': 50,
            'REPAIRING': 75,
            'COMPLETED': 100
        }
        
        progress = status_progress.get(complaint.status, 0)
        
        context = {
            'complaint': complaint,
            'progress': progress
        }
        return render(request, self.template_name, context)