from django import forms
# Import both models
from .models import Pole, TransformerCommissioning 

# --- 1. EXISTING FORM (Provisioning) ---

class PoleForm(forms.ModelForm):
    # This keeps your existing DateField setup
    commissioning_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Pole
        fields = '__all__'
        widgets = {
            'asset_class': forms.Select(),
            'asset_group': forms.Select(),
            'dmm': forms.Select(),
            'secondary_connection': forms.Select(),
        }

# --- 2. NEW FORM (Commissioning) ---

class TransformerCommissioningForm(forms.ModelForm):
    
    commissioning_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'text', 
                'placeholder': 'mm/dd/yyyy',
                'class': 'date-input-field'
            }
        ), 
        input_formats=['%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d'] 
    )

    class Meta:
        model = TransformerCommissioning
        fields = '__all__'
        
        widgets = {
            'actual_cost': forms.NumberInput(attrs={'placeholder': 'Enter Actual/Cost'}),
            'location': forms.Select(attrs={'placeholder': 'SELECT LOCATION'}), 
            
            # ADD THESE TWO LINES
            'latitude': forms.NumberInput(attrs={'placeholder': 'Enter Latitude (e.g., 8.7832)', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'placeholder': 'Enter Longitude (e.g., 76.7231)', 'step': '0.000001'}),
            
            'commissioning_payaze': forms.TextInput(attrs={'placeholder': 'Enter Commissioning Payaze'}), 
            'dmm': forms.Select(attrs={'class': 'select-box'}),
            'secondary_connection': forms.Select(attrs={'class': 'select-box'}),
            'ct_ratio': forms.TextInput(attrs={'placeholder': 'Enter CT Ratio'}),
            'pt_ratio': forms.TextInput(attrs={'placeholder': 'Enter PT Ratio'}),
        }
        
        labels = {
            'dmm': 'DMM',
            'secondary_connection': 'Secondary Connection',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
        }
        