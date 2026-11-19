from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    VILLAGER = 'VILLAGER', 'Villager'
    PANCHAYAT_ADMIN = 'PANCHAYAT_ADMIN', 'Panchayat Admin / Sarpanch'
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="Mobile number")
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.VILLAGER,
        help_text="Role determining permissions in the platform"
    )
    village = models.ForeignKey(
        'village.Village',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    ward = models.ForeignKey(
        'village.Ward',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False, help_text="Designates whether this villager/user identity is verified")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_villager(self):
        return self.role == UserRole.VILLAGER

    @property
    def is_panchayat_admin(self):
        return self.role == UserRole.PANCHAYAT_ADMIN or self.is_staff or self.is_superuser

    @property
    def is_superadmin(self):
        return self.role == UserRole.SUPER_ADMIN or self.is_superuser

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.username} - {self.get_role_display()})"
        return f"{self.username} ({self.get_role_display()})"
