from django.contrib import admin

# Register your models here.
from . models import User , Approval ,ApprovalMapping , AILearningExample,ApprovalInfo

admin.site.register(User)
admin.site.register(Approval)
admin.site.register(ApprovalMapping)
admin.site.register(AILearningExample)
admin.site.register(ApprovalInfo)