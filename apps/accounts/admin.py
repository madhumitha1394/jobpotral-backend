from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RecruiterProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 
                    'user_type', 'is_verified', 'is_staff']
    list_filter = ['user_type', 'is_verified', 'is_staff', 'created_at']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone', 'is_verified')}),
    )

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'industry', 'is_approved', 'location']
    list_filter = ['is_approved', 'industry']
    search_fields = ['company_name', 'user__email']