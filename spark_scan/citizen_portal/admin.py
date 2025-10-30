# citizen_portal/admin.py
from django.contrib import admin
from .models import Complaint, ComplaintImage


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_id', 'pole', 'safety_hazard', 'mobile_number', 'status', 'otp_verified', 'created_at']
    list_filter = ['status', 'safety_hazard', 'otp_verified']
    search_fields = ['pole__asset_number', 'mobile_number']  
    readonly_fields = ['complaint_id', 'created_at']

@admin.register(ComplaintImage)
class ComplaintImageAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'uploaded_at']