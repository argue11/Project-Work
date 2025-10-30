from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse 
from .forms import PoleForm, TransformerCommissioningForm 
# You may need to import location models or utilities for real coordinate data later

# --- 1. EXISTING VIEW (Provisioning) ---
class AddPole(View):
    form_class = PoleForm
    # Assuming your provisioning template is here
    template_name = 'asset/add_pole.html' 

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            "page": "add-pole",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")  
        context = {
            "page": "add-pole",
            "form": form
        }
        return render(request, self.template_name, context)


# --- 2. NEW VIEW (Commissioning) ---

class CommissionTransformer(View):
    form_class = TransformerCommissioningForm
    template_name = 'asset/commission_transformer.html' # Adopts template_name attribute
    
    # Define initial map data (similar to how MapView defines bounds)
    initial_map_data = {
        # Coordinates for New York (as shown in the image)
        'initial_lat': 40.7128, 
        'initial_lon': -74.0060,
        'initial_zoom': 13,
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            "page": "commission-transformer",
            "form": form,
            **self.initial_map_data # Pass map data to the template
        }
        return render(request, self.template_name, context) 

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the success URL
            return redirect("commissioning_success") 
        
        context = {
            "page": "commission-transformer",
            "form": form,
            **self.initial_map_data 
        }
        return render(request, self.template_name, context)


# --- 3. NEW SUCCESS VIEW ---

def commissioning_success(request):
    """A simple success page after transformer commissioning."""
    return HttpResponse("<h1>Transformer Commissioned Successfully!</h1><p>Data saved to the database.</p>")