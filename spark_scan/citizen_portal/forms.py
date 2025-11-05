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


class ComplaintResolutionForm(forms.ModelForm):
    """Form for operators to resolve complaints"""
    class Meta:
        model = Complaint
        fields = ['status', 'resolution_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control status-select',
                'required': True
            }),
            'resolution_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the resolution steps taken...\n\nExample:\n- Inspected the pole and found loose connections\n- Tightened all electrical connections\n- Replaced damaged wire insulation\n- Tested the light - now working properly\n- Area secured and cleaned',
                'rows': 8,
                'required': True
            })
        }
        labels = {
            'status': 'Update Status',
            'resolution_notes': 'Resolution Details'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize status choices to show only valid progression
        current_status = self.instance.status if self.instance else 'SUBMITTED'
        
        # Define valid status transitions
        if current_status == 'SUBMITTED':
            self.fields['status'].choices = [
                ('INSPECTING', 'Inspecting'),
                ('REPAIRING', 'Repairing'),
                ('COMPLETED', 'Completed'),
            ]
        elif current_status == 'INSPECTING':
            self.fields['status'].choices = [
                ('INSPECTING', 'Inspecting'),
                ('REPAIRING', 'Repairing'),
                ('COMPLETED', 'Completed'),
            ]
        elif current_status == 'REPAIRING':
            self.fields['status'].choices = [
                ('REPAIRING', 'Repairing'),
                ('COMPLETED', 'Completed'),
            ]
        else:
            self.fields['status'].choices = [
                ('COMPLETED', 'Completed'),
            ]
    
    def clean_resolution_notes(self):
        notes = self.cleaned_data.get('resolution_notes')
        if not notes or len(notes.strip()) < 20:
            raise forms.ValidationError('Please provide detailed resolution notes (minimum 20 characters).')
        return notes
    
    def clean_status(self):
        status = self.cleaned_data.get('status')
        if not status:
            raise forms.ValidationError('Please select a status.')
        return status