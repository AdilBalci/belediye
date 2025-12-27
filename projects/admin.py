from django.contrib import admin
from .models import PermitProject

@admin.register(PermitProject)
class PermitProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'applicant_name', 'status', 'assigned_engineer', 'created_at')
    list_filter = ('status',)
