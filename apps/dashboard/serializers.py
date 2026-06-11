from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, Q
from django.utils import timezone
from apps.jobs.models import Job
from apps.applications.models import JobApplication

User = get_user_model()

class DashboardStatsSerializer(serializers.Serializer):
    total_jobs = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    total_candidates = serializers.IntegerField()
    total_recruiters = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    hired_count = serializers.IntegerField()
    rejected_count = serializers.IntegerField()
    active_jobs = serializers.IntegerField()

class MonthlyStatsSerializer(serializers.Serializer):
    month = serializers.CharField()
    jobs_posted = serializers.IntegerField()
    applications_received = serializers.IntegerField()
    hires = serializers.IntegerField()

class RecentActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    user = serializers.CharField()

class AdminDashboardSerializer(serializers.Serializer):
    stats = DashboardStatsSerializer()
    monthly_stats = MonthlyStatsSerializer(many=True)
    recent_activities = RecentActivitySerializer(many=True)

class RecruiterDashboardSerializer(serializers.Serializer):
    total_jobs = serializers.IntegerField()
    active_jobs = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    new_applications = serializers.IntegerField()
    interviews_scheduled = serializers.IntegerField()
    hires = serializers.IntegerField()
    monthly_stats = MonthlyStatsSerializer(many=True)
    recent_applications = serializers.SerializerMethodField()
    
    def get_recent_applications(self, obj):
        applications = JobApplication.objects.filter(
            job__recruiter=obj['recruiter']
        ).select_related('applicant', 'job').order_by('-applied_at')[:5]
        
        return [{
            'id': app.id,
            'applicant_name': app.applicant.get_full_name(),
            'job_title': app.job.title,
            'status': app.status,
            'applied_at': app.applied_at
        } for app in applications]