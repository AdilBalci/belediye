from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'assigned_unit', 'created_at')
    list_filter = ('status', 'assigned_unit')
    search_fields = ('title', 'description')
