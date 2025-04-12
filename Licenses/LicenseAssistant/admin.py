from django.contrib import admin

# Register your models here.
from . models import User ,BusinessProfile , Approval

admin.site.register(User)
admin.site.register(Approval)
admin.site.register(BusinessProfile)
