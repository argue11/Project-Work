from django.urls import path
from .views import MapView

app_name = "dashboard"

urlpatterns = [
    path('', MapView.as_view(), name='leaflet-map'),
]
