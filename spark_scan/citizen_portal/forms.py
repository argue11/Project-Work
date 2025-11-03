from django import forms
from .models import Complaint

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+91 98765 43210',
            'pattern': r'^\+?[1-9]\d{9,14}$'
        }),
        label='Mobile Number',
        help_text='Enter with country code (e.g., +917559942623)'
    )

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-input otp-input',
            'placeholder': '000000',
            'maxlength': '6',
            'autocomplete': 'off'
        }),
        label='Enter OTP'
    )

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'complaint_description',
            'severity',
            'image1',
            'image2',
            'reporter_name'
        ]
        widgets = {
            'complaint_description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe the issue clearly...\n\nExample: The pole at the corner of Oak Street and 5th Ave is leaning precariously, and there are frayed wires hanging low, sparking intermittently.',
                'rows': 6
            }),
            'severity': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image1': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/jpeg,image/png,image/jpg',
                'capture': 'environment'  # Opens camera on mobile
            }),
            'image2': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/jpeg,image/png,image/jpg',
                'capture': 'environment'
            }),
            'reporter_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name (Optional)'
            })
        }
        labels = {
            'complaint_description': 'Complaint Description',
            'severity': 'Safety Hazard Level',
            'image1': 'Photo 1',
            'image2': 'Photo 2 (Optional)',
            'reporter_name': 'Your Name (Optional)'
        }