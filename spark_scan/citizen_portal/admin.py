from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_id', 'asset', 'reporter_phone', 'severity', 'status', 'created_at']
    list_filter = ['status', 'severity', 'created_at']
    search_fields = ['complaint_id', 'reporter_phone', 'complaint_description']
    readonly_fields = ['complaint_id', 'created_at', 'updated_at']