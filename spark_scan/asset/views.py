from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Asset
from .forms import ProvisioningForm, CommissioningForm

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db.models import Count, Q
from .models import Asset
from .forms import ProvisioningForm, CommissioningForm


class AssetDashboardView(View):
    """Unified dashboard with workflow tabs"""
    template_name = 'asset/asset_dashboard.html'
    
    def get(self, request,*args,**kwargs):
        # Get active tab from query parameter
        active_tab = kwargs.get('tab', request.GET.get('tab', 'all'))
        
        # Filter assets based on active tab
        if active_tab == 'provisioned':
            assets = Asset.objects.filter(status='PROVISIONED')
        elif active_tab == 'commissioned':
            assets = Asset.objects.filter(status='COMMISSIONED')
        else:
            assets = Asset.objects.all()
        
        # Get counts for stats
        total_assets = Asset.objects.count()
        provisioned_count = Asset.objects.filter(status='PROVISIONED').count()
        commissioned_count = Asset.objects.filter(status='COMMISSIONED').count()
        
        context = {
            'assets': assets,
            'active_tab': active_tab,
            'total_assets': total_assets,
            'provisioned_count': provisioned_count,
            'commissioned_count': commissioned_count,
        }
        return render(request, self.template_name, context)


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
            return redirect('asset:provisioned_list')
        
        context = {
            'form': form,
            'page_title': 'Provision New Asset'
        }
        return render(request, self.template_name, context)


class ProvisionedAssetsListView(View):
    """View to list all provisioned assets waiting for commissioning"""
    template_name = 'asset/provisioned_list.html'
    
    def get(self, request):
        assets = Asset.objects.filter(status='PROVISIONED')
        context = {
            'assets': assets,
            'page_title': 'Provisioned Assets'
        }
        return render(request, self.template_name, context)


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
            return redirect('asset:commissioned_list')
        
        context = {
            'form': form,
            'asset': asset,
            'page_title': f'Commission Asset - {asset.asset_number}'
        }
        return render(request, self.template_name, context)


class CommissionedAssetsListView(View):
    """View to list all commissioned assets"""
    template_name = 'asset/commissioned_list.html'
    
    def get(self, request):
        assets = Asset.objects.filter(status='COMMISSIONED')
        context = {
            'assets': assets,
            'page_title': 'Commissioned Assets'
        }
        return render(request, self.template_name, context)
    

