from django.contrib import admin
from .models import Job, JobCategory, SavedJob

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'recruiter', 'category', 'job_type', 'experience_level', 
                    'status', 'location', 'created_at']
    list_filter = ['status', 'job_type', 'experience_level', 'is_remote', 'created_at']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'created_at'

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'saved_at']
    list_filter = ['saved_at']