from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import qrcode
from io import BytesIO
import base64

from .models import Asset
from .forms import ProvisioningForm, CommissioningForm
from authentication.permissions import permission_roles


# NEW: Asset List View for Actions button
class AssetListView(View):
    """View to list all assets with role-based actions"""
    template_name = 'asset/asset_list.html'
    
    def get(self, request):
        assets = Asset.objects.all().order_by('-created_at')
        
        context = {
            'assets': assets,
            'page_title': 'Asset Management'
        }
        return render(request, self.template_name, context)


@method_decorator(permission_roles(roles=['Officer']), name='dispatch')    
class ProvisionAssetView(View):
    """View for provisioning new assets"""
    template_name = 'asset/provision_asset.html'
    form_class = ProvisioningForm
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form': form,
            'page_title': 'Provision New Asset'
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f'Asset {asset.asset_number} provisioned successfully!')
            return redirect('asset:asset_list')
        
        context = {
            'form': form,
            'page_title': 'Provision New Asset'
        }
        return render(request, self.template_name, context)


# NEW: Edit Asset View (Officer only)
@method_decorator(permission_roles(roles=['Officer']), name='dispatch')
class EditAssetView(View):
    """View for editing an existing asset"""
    template_name = 'asset/edit_asset.html'
    form_class = ProvisioningForm
    
    def get(self, request, asset_id):
        asset = get_object_or_404(Asset, id=asset_id)
        form = self.form_class(instance=asset)
        context = {
            'form': form,
            'asset': asset,
            'page_title': f'Edit Asset - {asset.asset_number}'
        }
        return render(request, self.template_name, context)
    
    def post(self, request, asset_id):
        asset = get_object_or_404(Asset, id=asset_id)
        form = self.form_class(request.POST, instance=asset)
        
        if form.is_valid():
            updated_asset = form.save()
            messages.success(request, f'Asset {updated_asset.asset_number} updated successfully!')
            return redirect('asset:asset_list')
        
        context = {
            'form': form,
            'asset': asset,
            'page_title': f'Edit Asset - {asset.asset_number}'
        }
        return render(request, self.template_name, context)


# NEW: Delete Asset (Officer only)
@require_http_methods(["POST"])
@permission_roles(roles=['Officer'])
def delete_asset(request, asset_id):
    """Delete an asset (AJAX endpoint)"""
    try:
        asset = get_object_or_404(Asset, id=asset_id)
        asset_number = asset.asset_number
        asset.delete()
        return JsonResponse({
            'success': True,
            'message': f'Asset {asset_number} deleted successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# NEW: View QR Code (All roles)
@require_http_methods(["POST"])
def view_qr_code(request, asset_id):
    """Generate and return QR code for asset complaint URL (AJAX endpoint)"""
    try:
        asset = get_object_or_404(Asset, id=asset_id)
        
        # Check if asset is commissioned
        if asset.status != 'COMMISSIONED':
            return JsonResponse({
                'success': False,
                'error': 'not_commissioned',
                'message': 'Asset is not commissioned yet. QR code can only be generated for commissioned assets.'
            }, status=400)
        
        # Build the complaint registration URL
        complaint_url = request.build_absolute_uri(
            reverse('citizen_portal:report_step1', kwargs={'asset_id': asset.id})
        )
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(complaint_url)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for sending to frontend
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return JsonResponse({
            'success': True,
            'qr_code': f'data:image/png;base64,{img_base64}',
            'asset_number': asset.asset_number,
            'complaint_url': complaint_url
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@method_decorator(permission_roles(roles=['Operator']), name='dispatch')    
class CommissionAssetView(View):
    """View for commissioning a provisioned asset"""
    template_name = 'asset/commission_asset.html'
    form_class = CommissioningForm
    
    def get(self, request, asset_id):
        asset = get_object_or_404(Asset, id=asset_id, status='PROVISIONED')
        form = self.form_class()
        context = {
            'form': form,
            'asset': asset,
            'page_title': f'Commission Asset - {asset.asset_number}'
        }
        return render(request, self.template_name, context)
    
    def post(self, request, asset_id):
        asset = get_object_or_404(Asset, id=asset_id, status='PROVISIONED')
        form = self.form_class(request.POST, request.FILES, instance=asset)
        
        if form.is_valid():
            commissioned_asset = form.save()
            messages.success(request, f'Asset {commissioned_asset.asset_number} commissioned successfully!')
            return redirect('asset:asset_list')
        
        context = {
            'form': form,
            'asset': asset,
            'page_title': f'Commission Asset - {asset.asset_number}'
        }
        return render(request, self.template_name, context)


