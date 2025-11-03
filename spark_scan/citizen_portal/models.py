from django.db import models
from asset.models import Asset

class ComplaintStatus(models.TextChoices):
    SUBMITTED = 'SUBMITTED', 'Submitted'
    INSPECTING = 'INSPECTING', 'Inspecting'
    REPAIRING = 'REPAIRING', 'Repairing'
    COMPLETED = 'COMPLETED', 'Completed'

class SeverityLevel(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'

class Complaint(models.Model):
    # Complaint ID (auto-generated)
    complaint_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Linked Asset
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='complaints')
    
    # Reporter Information
    reporter_name = models.CharField(max_length=100, null=True, blank=True)
    reporter_phone = models.CharField(max_length=15)
    
    # Complaint Details
    complaint_description = models.TextField()
    severity = models.CharField(max_length=20, choices=SeverityLevel.choices, default='MEDIUM')
    
    # Images
    image1 = models.ImageField(upload_to='complaint_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='complaint_images/', null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=ComplaintStatus.choices, default='SUBMITTED')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    resolution_notes = models.TextField(null=True, blank=True)
    resolved_by = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
    
    def __str__(self):
        return f"{self.complaint_id} - {self.asset.asset_number}"
    
    def save(self, *args, **kwargs):
        if not self.complaint_id:
            self.complaint_id = self.generate_complaint_id()
        super().save(*args, **kwargs)
    
    def generate_complaint_id(self):
        import random
        from datetime import datetime
        year = datetime.now().year
        while True:
            complaint_id = f"CPN-{year}-{random.randint(1000, 9999)}"
            if not Complaint.objects.filter(complaint_id=complaint_id).exists():
                return complaint_id