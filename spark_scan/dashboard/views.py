from django.shortcuts import render
from django.views import View
from django.db.models import Count, Q
from asset.models import Asset
from citizen_portal.models import Complaint
import json

class MapView(View):
    template_name = 'dashboard/map.html'
    
    def get(self, request, *args, **kwargs):
        # Get COMMISSIONED assets with GPS coordinates and annotate with complaint counts
        commissioned_assets = Asset.objects.filter(
            status='COMMISSIONED',
            latitude__isnull=False,
            longitude__isnull=False
        ).annotate(
            open_complaints=Count(
                'complaints',
                filter=Q(complaints__status__in=['SUBMITTED', 'INSPECTING', 'REPAIRING'])
            ),
            total_complaints=Count('complaints')
        )
        
        # Separate poles and transformers
        poles = commissioned_assets.filter(asset_type='POLE')
        transformers = commissioned_assets.filter(asset_type='TRANSFORMER')
        
        # Prepare poles data for JavaScript
        poles_data = []
        for pole in poles:
            poles_data.append({
                'id': pole.id,
                'lat': float(pole.latitude),
                'lng': float(pole.longitude),
                'asset_number': pole.asset_number,
                'location': pole.actual_location or pole.planned_location or 'Unknown',
                'commissioning_date': pole.commissioning_date.strftime('%Y-%m-%d') if pole.commissioning_date else 'N/A',
                'status': pole.get_status_display(),
                'has_complaints': pole.open_complaints > 0,
                'open_complaints': pole.open_complaints,
                'total_complaints': pole.total_complaints,
            })
        
        # Prepare transformers data for JavaScript
        transformers_data = []
        for transformer in transformers:
            transformers_data.append({
                'id': transformer.id,
                'lat': float(transformer.latitude),
                'lng': float(transformer.longitude),
                'asset_number': transformer.asset_number,
                'location': transformer.actual_location or transformer.planned_location or 'Unknown',
                'commissioning_date': transformer.commissioning_date.strftime('%Y-%m-%d') if transformer.commissioning_date else 'N/A',
                'actual_cost': str(transformer.actual_cost) if transformer.actual_cost else 'N/A',
                'has_complaints': transformer.open_complaints > 0,
                'open_complaints': transformer.open_complaints,
                'total_complaints': transformer.total_complaints,
            })
        
        # Calculate complaint statistics
        all_complaints = Complaint.objects.all()
        opened_count = all_complaints.filter(status='SUBMITTED').count()
        active_count = all_complaints.filter(status__in=['INSPECTING', 'REPAIRING']).count()
        closed_count = all_complaints.filter(status='COMPLETED').count()
        
        context = {
            'poles': json.dumps(poles_data),
            'transformers': json.dumps(transformers_data),
            'opened_count': opened_count,
            'active_count': active_count,
            'closed_count': closed_count,
        }
        return render(request, self.template_name, context)