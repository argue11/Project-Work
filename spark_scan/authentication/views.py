from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
import threading

from .forms import LoginForm, RegisterForm, OTPForm, NewPasswordForm
from .utility import password_generator, sending_email, generate_otp, send_phone_sms
from .permissions import permission_roles
from .models import OTP, Profile

class LoginView(View):
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        data = {"form": form}
        return render(request, "authentication/login.html", context=data)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(**form.cleaned_data)

            if user:
                login(request, user)
                return redirect("leaflet-map")
            
            msg = "Invalid Credentials"

        context = {"form": form, "msg": msg if "msg" in locals() else None}
        return render(request, "authentication/login.html", context)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("public_dashboard:public_map")


# ========================================
# OFFICER/OPERATOR REGISTRATION VIEWS
# ========================================

class OfficerRegisterView(View):
    form_class = RegisterForm
    template_name = 'authentication/register_officer.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.role = "Officer"  # Set role as Officer

            password = password_generator()
            print(f"Officer Password: {password}")

            user.password = make_password(password)
            user.save()

            # Send credentials via email
            subject = "Officer Account Credentials"
            template = "email/login-credentials.html"
            context = {"user": user, "password": password, "role": "Officer"}
            recipient = user.email

            thread = threading.Thread(target=sending_email, args=(subject, template, context, recipient))
            thread.start()

            messages.success(request, "Acccount created successfully! Credentials sent via email.")
            return redirect("authentication:login")
        
        context = {"form": form}
        return render(request, self.template_name, context)

class OperatorRegisterView(View):
    form_class = RegisterForm
    template_name = 'authentication/register_operator.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.role = "Operator"  # Set role as Operator

            password = password_generator()
            print(f"Operator Password: {password}")

            user.password = make_password(password)
            user.save()

            # Send credentials via email
            subject = "Operator Account Credentials"
            template = "email/login-credentials.html"
            context = {"user": user, "password": password, "role": "Operator"}
            recipient = user.email

            thread = threading.Thread(target=sending_email, args=(subject, template, context, recipient))
            thread.start()

            messages.success(request, "Account created successfully! Credentials sent via email.")
            return redirect("authentication:login")
        
        context = {"form": form}
        return render(request, self.template_name, context)

# ========================================
# PASSWORD MANAGEMENT VIEWS (FIXED)
# ========================================

@method_decorator(permission_roles(roles=['Officer', 'Operator']), name='dispatch')     
class ChangePasswordView(View):
    form_class = OTPForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        # Generate OTP
        email_otp, phone_otp = generate_otp()  # Assuming this returns tuple

        # Get or create OTP record for user
        otp, status = OTP.objects.get_or_create(user=request.user)
        otp.email_otp = email_otp
        otp.phone_otp = phone_otp
        otp.verified = False
        otp.save()

        # Send email OTP
        subject = 'OTP For Change Password'
        template = 'email/email-otp.html'
        context = {'otp': email_otp, 'request': request}
        recipient = request.user.email

        thread = threading.Thread(target=sending_email, args=(subject, template, context, recipient))
        thread.start()

        # Send SMS OTP
        send_phone_sms(request.user.phone_num, phone_otp)

        request.session["otp_time"] = timezone.now().timestamp()
        remaining_time = 600
        
        data = {'form': form, "remaining_time": remaining_time}
        return render(request, 'authentication/otp.html', context=data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            validated_data = form.cleaned_data
            email_otp = validated_data.get("email_otp")
            phone_otp = validated_data.get("phone_otp")
            otp_time = request.session.get("otp_time")

            error = None

            try:
                otp = OTP.objects.get(user=request.user)
                db_email_otp = otp.email_otp
                db_phone_otp = otp.phone_otp

                if otp_time:
                    elapsed = timezone.now().timestamp() - otp_time
                    remaining_time = max(0, 600 - int(elapsed))

                    if elapsed > 600:
                        error = "OTP expired, request a new one"
                    elif email_otp == db_email_otp and phone_otp == db_phone_otp:
                        request.session.pop("otp_time")
                        otp.verified = True
                        otp.save()
                        return redirect("authentication:new-password")
                    else:
                        error = "Invalid OTP"
            except OTP.DoesNotExist:
                error = "OTP not found"

        data = {'form': form, "remaining_time": remaining_time if 'remaining_time' in locals() else 600, "error": error}
        return render(request, 'authentication/otp.html', context=data)

@method_decorator(permission_roles(roles=['Officer', 'Operator']), name="dispatch")
class NewPasswordView(View):
    form_class = NewPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, "authentication/new-password.html", context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = request.user
            user.password = make_password(password)
            user.save()

            logout(request)
            messages.success(request, "Password successfully changed")
            return redirect("authentication:login")            

        context = {"form": form}
        return render(request, "authentication/new-password.html", context)

# ========================================
# GENERIC OTP VIEWS (For Citizen Portal)
# ========================================

class SendOTPView(View):
    """Generic view to send OTP to phone number (for guest users)"""
    
    def post(self, request, *args, **kwargs):
        phone_number = request.POST.get('phone_number')
        
        if not phone_number:
            return JsonResponse({'success': False, 'error': 'Phone number required'})
        
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
        
        # Send SMS in background
        thread = threading.Thread(target=send_phone_sms, args=(phone_number, otp_code))
        thread.start()
        
        # Store in session
        request.session['otp_phone'] = phone_number
        request.session['otp_time'] = timezone.now().timestamp()
        
        return JsonResponse({'success': True, 'message': 'OTP sent successfully'})

class VerifyOTPView(View):
    """Generic view to verify OTP (for guest users)"""
    
    def post(self, request, *args, **kwargs):
        phone_number = request.session.get('otp_phone')
        entered_otp = request.POST.get('otp')
        
        if not phone_number or not entered_otp:
            return JsonResponse({'success': False, 'error': 'Invalid request'})
        
        try:
            otp_record = OTP.objects.get(phone_number=phone_number, phone_otp=entered_otp)
            
            if otp_record.is_expired():
                return JsonResponse({'success': False, 'error': 'OTP expired'})
            
            # Mark as verified
            otp_record.verified = True
            otp_record.save()
            
            request.session['otp_verified'] = True
            
            return JsonResponse({'success': True, 'message': 'OTP verified successfully'})
            
        except OTP.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid OTP'})