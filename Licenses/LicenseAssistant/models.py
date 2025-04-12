from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="license_assistant_users"  # Added related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="license_assistant_user_permissions"  # Added related_name
    )
    pass 

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="usersbusiness")
    business_name = models.CharField(max_length=100)
    business_structure = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # Add more fields as needed

class Approval(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    description = models.TextField()
    api_available = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    
    
