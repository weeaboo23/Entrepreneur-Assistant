from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.text import slugify

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



class Approval(models.Model):
    name = models.CharField(max_length=100)
    api_available = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Automatically generate slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ApprovalInfo(models.Model):
    approval = models.OneToOneField(Approval, on_delete=models.CASCADE, related_name="licenseinfo")
    description = models.TextField()
    department = models.TextField()
    documents_required = models.TextField() 
    application_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"License Info for {self.approval.name}"


    


class ApprovalMapping(models.Model):
    structure = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    licenses = models.ManyToManyField(Approval, related_name="approval_mappings" , blank=True , null=True )


    class Meta:
        unique_together = ('structure', 'activity', 'location')
        indexes = [
            models.Index(fields=['structure']),
            models.Index(fields=['activity']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.structure} - {self.activity} - {self.location}"
    

class AILearningExample(models.Model):
    structure = models.CharField(max_length=255)
    activity = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    suggested_licenses = models.TextField()  # store as JSON
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.structure}, {self.activity}, {self.location}"


class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user if self.user else 'Anonymous'} - {self.subject}"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.approval.name} by {self.user.username}"


