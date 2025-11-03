from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleChoice(models.TextChoices):
    ADMIN = "Admin", "Admin"
    USER = "User", "User"

class Profile(AbstractUser):
    role = models.CharField(max_length=15, choices=RoleChoice.choices)
    phone_num = models.CharField(max_length=15, unique=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return f"{self.username}"


class OTP(models.Model):
    """Generic OTP model - can be used for any phone verification"""
    user = models.OneToOneField("Profile", on_delete=models.CASCADE, null=True, blank=True)
    
    # For guest users (citizen portal)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    phone_otp = models.CharField(max_length=6, null=True, blank=True)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"

    def __str__(self):
        if self.user:
            return f"{self.user.username} - OTP"
        return f"{self.phone_number} - OTP"
    
    def is_expired(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).total_seconds() > 600  # 10 minutes