from django.shortcuts import render,render

from django.shortcuts import render


from django.views import View
from django.shortcuts import render

class MapView(View):
    template_name = 'dashboard/map.html'
    
    def get(self, request, *args, **kwargs):
        rectangle_bounds = [[8.78, 76.72], [8.8, 76.74]]  # Example rectangle bounds
        
        context = {
            'rectangle_bounds': rectangle_bounds
        }
        return render(request, self.template_name, context)


