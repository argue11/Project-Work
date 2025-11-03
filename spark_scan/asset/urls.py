from django.urls import path
from . import views

app_name = 'asset'

urlpatterns = [
    # Dashboard (shows all assets with tabs)
    path('', views.AssetDashboardView.as_view(), name='dashboard'),
    
    # Provisioning
    path('provision/', views.ProvisionAssetView.as_view(), name='provision'),
    
    # These two are just aliases pointing back to dashboard with specific tabs
    path('provisioned/', views.AssetDashboardView.as_view(), {'tab': 'provisioned'}, name='provisioned_list'),
    path('commissioned/', views.AssetDashboardView.as_view(), {'tab': 'commissioned'}, name='commissioned_list'),
    
    # Commissioning
    path('commission/<int:asset_id>/', views.CommissionAssetView.as_view(), name='commission'),
]