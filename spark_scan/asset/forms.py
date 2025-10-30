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
    
    # Custom widget for DateField to match the 'mm/dd/yy/y' placeholder in the image
    commissioning_date = forms.DateField(
        widget=forms.DateInput(
            # Using type 'text' to show the placeholder format clearly, 
            # and setting the placeholder text.
            attrs={
                'type': 'text', 
                'placeholder': 'mm/dd/yyyy',
                'class': 'date-input-field' # Add a class for specific styling if needed
            }
        ), 
        # Define accepted input formats for processing the data
        input_formats=['%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d'] 
    )

    class Meta:
        model = TransformerCommissioning
        fields = '__all__' # Include all fields from the new model
        
        # Customize widgets for better styling and placeholders based on the image
        widgets = {
            'actual_cost': forms.NumberInput(attrs={'placeholder': 'Enter Actual/Cost'}),
            # Use Select for location dropdown (as per image)
            'location': forms.Select(attrs={'placeholder': 'SELECT LOCATION'}), 
            
            # Corresponds to 'Commissioning Payaze'
            'commissioning_payaze': forms.TextInput(attrs={'placeholder': 'Enter Commissioning Payaze'}), 
            
            'dmm': forms.Select(attrs={'class': 'select-box'}),
            'secondary_connection': forms.Select(attrs={'class': 'select-box'}),
            
            'ct_ratio': forms.TextInput(attrs={'placeholder': 'Enter CT Ratio'}),
            'pt_ratio': forms.TextInput(attrs={'placeholder': 'Enter PT Ratio'}),
        }
        
        # Custom labels if needed (e.g., if model verbose_name isn't sufficient)
        labels = {
            'dmm': 'DMM',
            'secondary_connection': 'Secondary Connection',
        }