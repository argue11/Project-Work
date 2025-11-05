from django import forms
from .models import Asset

class ProvisioningForm(forms.ModelForm):
    """Form for provisioning assets (planning phase)"""
    
    provisioning_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Asset
        fields = [
            'asset_type',
            'asset_number',
            'asset_group',
            'provisioning_date',
            'provisioned_by',
            'planned_location',
            'dmm',
            'secondary_connection',
            'ct_ratio',
            'pt_ratio',
        ]
        widgets = {
            'asset_type': forms.Select(attrs={'class': 'form-control'}),
            'asset_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., POLE-001'}),
            'asset_group': forms.Select(attrs={'class': 'form-control'}),
            'provisioned_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'planned_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe planned location'}),
            'dmm': forms.Select(attrs={'class': 'form-control'}),
            'secondary_connection': forms.Select(attrs={'class': 'form-control'}),
            'ct_ratio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 100:5'}),
            'pt_ratio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 11000:110'}),
        }
        labels = {
            'asset_type': 'Asset Type',
            'asset_number': 'Asset Number',
            'asset_group': 'Asset Group',
            'provisioning_date': 'Provisioning Date',
            'provisioned_by': 'Provisioned By',
            'planned_location': 'Planned Location',
            'dmm': 'DMM',
            'secondary_connection': 'Secondary Connection',
            'ct_ratio': 'CT Ratio',
            'pt_ratio': 'PT Ratio',
        }


class CommissioningForm(forms.ModelForm):
    """Form for commissioning assets (installation phase)"""
    
    commissioning_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Asset
        fields = [
            'commissioning_date',
            'commissioned_by',
            'actual_location',
            'latitude',
            'longitude',
            'actual_cost',
            'qr_code',
        ]
        widgets = {
            'commissioned_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'actual_location': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Actual installed location'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 8.8932', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 76.6141', 'step': '0.000001'}),
            'actual_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 25000.00'}),
            'qr_code': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'commissioning_date': 'Commissioning Date',
            'commissioned_by': 'Commissioned By',
            'actual_location': 'Actual Location',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'actual_cost': 'Actual Cost (₹)',
            'qr_code': 'QR Code Image',
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Automatically change status to COMMISSIONED
        instance.status = 'COMMISSIONED'
        if commit:
            instance.save()
        return instance
    
