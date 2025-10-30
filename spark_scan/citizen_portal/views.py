# citizen_portal/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from asset.models import Pole  # ← CHANGE THIS: Import from your asset app
from .models import Complaint, ComplaintImage  # ← Keep these from citizen_portal
import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

class ComplaintFormView(View):
    """Show complaint form when user scans QR code"""
    
    def get(self, request, asset_id):
        # CHANGE: Use asset_number instead of asset_id
        pole = get_object_or_404(Pole, asset_number=asset_id)  # ← CHANGE THIS
        context = {
            'pole': pole,
            'safety_hazards': Complaint.SAFETY_HAZARDS
        }
        return render(request, 'citizen_portal/complaint_form.html', context)
    
    def post(self, request, asset_id):
        # CHANGE: Use asset_number instead of asset_id
        pole = get_object_or_404(Pole, asset_number=asset_id)  # ← CHANGE THIS
        
        # Get form data
        mobile_number = request.POST.get('mobile_number')
        safety_hazard = request.POST.get('safety_hazard')
        description = request.POST.get('description')
        
        # Create complaint
        complaint = Complaint.objects.create(
            pole=pole,  # This links to your existing Pole model
            mobile_number=mobile_number,
            safety_hazard=safety_hazard,
            description=description
        )
        
        # Generate OTP
        complaint.generate_otp()
        print(f"📱 OTP for {mobile_number}: {complaint.otp}")
        
        # Handle image uploads
        images = request.FILES.getlist('images')
        for image in images:
            ComplaintImage.objects.create(complaint=complaint, image=image)
        
        return redirect('citizen_portal:verify_otp', complaint_id=complaint.complaint_id)

class VerifyOTPView(View):
    """OTP verification page"""
    
    def get(self, request, complaint_id):
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        context = {'complaint': complaint}
        return render(request, 'citizen_portal/verify_otp.html', context)
    
    def post(self, request, complaint_id):
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        entered_otp = request.POST.get('otp')
        
        success, message = complaint.verify_otp(entered_otp)
        
        if success:
            complaint.otp_verified = True
            complaint.status = 'PENDING'
            complaint.save()
            return redirect('citizen_portal:complaint_success')
        else:
            context = {
                'complaint': complaint,
                'error': message
            }
            return render(request, 'citizen_portal/verify_otp.html', context)

class ComplaintSuccessView(View):
    """Success page after OTP verification"""
    
    def get(self, request):
        return render(request, 'citizen_portal/complaint_success.html')

class ResendOTPView(View):
    """Resend OTP via AJAX"""
    
    def post(self, request, complaint_id):
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        complaint.generate_otp()
        
        print(f"🔄 New OTP for {complaint.mobile_number}: {complaint.otp}")
        
        return JsonResponse({
            'status': 'success', 
            'message': 'New OTP sent to your mobile number.'
        })

class ComplaintStatusView(View):
    """Check complaint status"""
    
    def get(self, request, complaint_id):
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        context = {'complaint': complaint}
        return render(request, 'citizen_portal/complaint_status.html', context)
    
def generate_pole_qr(request, asset_number):
    """Simple QR code generator for a pole"""
    pole = get_object_or_404(Pole, asset_number=asset_number)
    
    # Create URL that will open when QR is scanned
    qr_url = f"http://127.0.0.1:8000/report/{asset_number}/"
    
    # Generate QR code
    qr = qrcode.make(qr_url)
    
    # Return as image
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response