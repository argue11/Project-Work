from django.shortcuts import render
from django.views import View
from asset.models import Pole, TransformerCommissioning
import json

class MapView(View):
    template_name = 'dashboard/map.html'
    
    def get(self, request, *args, **kwargs):
        # Get poles with location data
        poles = Pole.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        )
        
        # Get transformers with location data
        transformers = TransformerCommissioning.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        )
        
        # Prepare poles data for JavaScript
        poles_data = []
        for pole in poles:
            poles_data.append({
                'id': pole.id,
                'lat': float(pole.latitude),
                'lng': float(pole.longitude),
                'asset_number': pole.asset_number,
                'location': pole.location or 'Unknown',
                'commissioning_date': pole.commissioning_date.strftime('%Y-%m-%d'),
                'status': pole.get_status_display(),
            })
        
        # Prepare transformers data for JavaScript
        transformers_data = []
        for transformer in transformers:
            transformers_data.append({
                'id': transformer.id,
                'lat': float(transformer.latitude),
                'lng': float(transformer.longitude),
                'location': transformer.location,
                'commissioning_date': transformer.commissioning_date.strftime('%Y-%m-%d'),
                'actual_cost': str(transformer.actual_cost),
            })
        
        context = {
            'poles': json.dumps(poles_data),
            'transformers': json.dumps(transformers_data),
        }
        return render(request, self.template_name, context)