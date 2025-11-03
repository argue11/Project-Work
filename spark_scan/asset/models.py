from django.db import models

# --- CHOICES ---
ASSET_TYPE_CHOICES = [
    ('POLE', 'Pole'),
    ('TRANSFORMER', 'Transformer'),
]

ASSET_GROUP_CHOICES = [
    ('UPDO', 'UPDO'),
]

DMM_CHOICES = [
    ('Option1', 'Option1'),
    ('Option2', 'Option2'),
]

SECONDARY_CONNECTION_CHOICES = [
    ('SC1', 'SC1'),
    ('SC2', 'SC2'),
    ('DELTA', 'Delta'),
    ('WYE', 'Wye'),
]

STATUS_CHOICES = [
    ('PROVISIONED', 'Provisioned'),
    ('COMMISSIONED', 'Commissioned'),
    ('INACTIVE', 'Inactive'),
    ('UNDER_MAINTENANCE', 'Under Maintenance'),
    ('FAULTY', 'Faulty'),
]


class Asset(models.Model):
    """
    Main model for all assets (Poles and Transformers).
    Handles both provisioning and commissioning phases.
    """
    # Basic Information
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)
    asset_number = models.CharField(max_length=50, unique=True)
    asset_group = models.CharField(max_length=10, choices=ASSET_GROUP_CHOICES)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROVISIONED')
    
    # Provisioning Phase (Planning)
    provisioning_date = models.DateField()
    provisioned_by = models.CharField(max_length=100)
    planned_location = models.TextField(help_text="Planned installation location description")
    
    # Commissioning Phase (Installation) - Initially NULL
    commissioning_date = models.DateField(null=True, blank=True)
    commissioned_by = models.CharField(max_length=100, null=True, blank=True)
    actual_location = models.TextField(null=True, blank=True, help_text="Actual installed location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Technical Specifications
    dmm = models.CharField(max_length=20, choices=DMM_CHOICES)
    secondary_connection = models.CharField(max_length=20, choices=SECONDARY_CONNECTION_CHOICES)
    ct_ratio = models.CharField(max_length=20)
    pt_ratio = models.CharField(max_length=20)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # QR Code (generated during commissioning)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_asset_type_display()} - {self.asset_number}"
    
    def is_commissioned(self):
        """Check if asset is commissioned"""
        return self.status == 'COMMISSIONED'
    
    def has_open_issues(self):
        """Check if asset has any open issues"""
        return self.issues.filter(status__in=['OPEN', 'IN_PROGRESS']).exists()