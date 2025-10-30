from django.urls import path
# Import all necessary views
from .views import AddPole, CommissionTransformer, commissioning_success 

urlpatterns = [
    # Existing Provisioning URL
    path('add-pole/', AddPole.as_view(), name='add_pole'),
    
    # New Commissioning URL
    path('commission-transformer/', CommissionTransformer.as_view(), name='commission_transformer'),
    
    # New Success URL
    path('commissioning-success/', commissioning_success, name='commissioning_success'),
]