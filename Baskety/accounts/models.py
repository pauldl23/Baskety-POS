from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cashier')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class UserSettings(models.Model):
    THEME_CHOICES = (
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default'),
    )
    LANDING_PAGE_CHOICES = (
        ('dashboard', 'Dashboard'),
        ('pos', 'POS'),
        ('inventory', 'Inventory'),
        ('reports', 'Reports'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    default_landing_page = models.CharField(max_length=20, choices=LANDING_PAGE_CHOICES, default='dashboard')
    theme_mode = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    compact_view = models.BooleanField(default=False)
    enable_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.user.username}"

# Signal to create UserSettings automatically when a User is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    if hasattr(instance, 'settings'):
        instance.settings.save()
    else:
        UserSettings.objects.get_or_create(user=instance)
