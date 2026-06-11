from django.contrib import admin
from .models import CandidateProfile, Skill, CandidateSkill, Experience, Education

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'headline', 'experience_level', 'location', 'is_open_to_work']
    list_filter = ['experience_level', 'is_open_to_work', 'created_at']
    search_fields = ['user__email', 'headline', 'location']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'skill', 'proficiency', 'years_experience']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job_title', 'company_name', 'start_date', 'is_current']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'institution', 'degree', 'field_of_study']