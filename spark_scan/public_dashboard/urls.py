from django.urls import path
from . import views

app_name = 'public_dashboard'

urlpatterns = [
    path('', views.PublicMapView.as_view(), name='public_map'),
]