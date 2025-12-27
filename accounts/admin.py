from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'phone_number')}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_superuser', 'is_active'] # removed is_staff as it might be conflicting with AbstractUser inheritance weirdness in admin check

admin.site.register(CustomUser, CustomUserAdmin)
