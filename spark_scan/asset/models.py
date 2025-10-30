from django.db import models

# --- CHOICES ---
ASSET_CLASS_CHOICES = [
    ('TRF', 'Transformer'),
    ('POL', 'Pole'),
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

# ▼▼▼ ADD THIS ▼▼▼
STATUS_CHOICES = [
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
    ('UNDER_MAINTENANCE', 'Under Maintenance'),
    ('FAULTY', 'Faulty'),
]
# ▲▲▲ ADD THIS ▲▲▲

class Pole(models.Model):
    # YOUR EXISTING FIELDS
    asset_class = models.CharField(max_length=10, choices=ASSET_CLASS_CHOICES)
    asset_group = models.CharField(max_length=10, choices=ASSET_GROUP_CHOICES)
    asset_number = models.CharField(max_length=50)
    commissioning_date = models.DateField()
    commissioning_person = models.CharField(max_length=100)
    dmm = models.CharField(max_length=20, choices=DMM_CHOICES)
    secondary_connection = models.CharField(max_length=20, choices=SECONDARY_CONNECTION_CHOICES)
    ct_ratio = models.CharField(max_length=20)
    pt_ratio = models.CharField(max_length=20)
    
    # ▼▼▼ ADD THESE 5 NEW FIELDS ▼▼▼
    location = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    # ▲▲▲ ADD THESE 5 NEW FIELDS ▲▲▲

    def __str__(self):
        return f"Provisioning: {self.asset_number} - {self.asset_class}"

class TransformerCommissioning(models.Model):
    # KEEP THIS EXACTLY AS IT IS
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Actual/Cost")
    location = models.CharField(max_length=100, verbose_name="Location")
    commissioning_date = models.DateField(verbose_name="Commissioning Date")
    commissioning_payaze = models.CharField(max_length=255, verbose_name="Commissioning Payaze")
    dmm = models.CharField(max_length=20, choices=DMM_CHOICES, verbose_name="DMM")
    secondary_connection = models.CharField(max_length=20, choices=SECONDARY_CONNECTION_CHOICES, verbose_name="Secondary Connection")
    ct_ratio = models.CharField(max_length=20, verbose_name="CT Ratio")
    pt_ratio = models.CharField(max_length=20, verbose_name="PT Ratio")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commissioning Record: {self.location} on {self.commissioning_date}"