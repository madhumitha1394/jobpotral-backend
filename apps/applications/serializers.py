from rest_framework import serializers
from .models import JobApplication, ApplicationStatusHistory
from apps.jobs.serializers import JobListSerializer

class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source='changed_by.get_full_name', read_only=True)
    
    class Meta:
        model = ApplicationStatusHistory
        fields = ['id', 'old_status', 'new_status', 'changed_by_name', 'notes', 'created_at']

class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    applicant_name = serializers.CharField(source='applicant.get_full_name', read_only=True)
    applicant_email = serializers.EmailField(source='applicant.email', read_only=True)
    status_history = ApplicationStatusHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'applied_at', 'updated_at']

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume', 'expected_salary', 'notice_period']
    
    def validate(self, attrs):
        request = self.context.get('request')
        job_id = self.context.get('job_id')
        
        if JobApplication.objects.filter(applicant=request.user, job_id=job_id).exists():
            raise serializers.ValidationError("You have already applied for this job")
        
        return attrs

class UpdateStatusSerializer(serializers.ModelSerializer):
    status_notes = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = JobApplication
        fields = ['status', 'status_notes', 'interview_date']