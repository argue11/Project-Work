from django.urls import path
from . import views

app_name = 'asset'

urlpatterns = [
    
    # NEW: Asset List (for Actions button)
    path('list/', views.AssetListView.as_view(), name='asset_list'),
    
    # Provisioning
    path('provision/', views.ProvisionAssetView.as_view(), name='provision'),
    
    # NEW: Edit Asset (Officer only)
    path('edit/<int:asset_id>/', views.EditAssetView.as_view(), name='edit_asset'),
    
    # NEW: Delete Asset (Officer only)
    path('delete/<int:asset_id>/', views.delete_asset, name='delete_asset'),
    
    # NEW: View QR Code (All roles)
    path('view-qr/<int:asset_id>/', views.view_qr_code, name='view_qr'),
    
    # Commissioning
    path('commission/<int:asset_id>/', views.CommissionAssetView.as_view(), name='commission'),
]