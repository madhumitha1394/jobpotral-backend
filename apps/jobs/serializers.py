from rest_framework import serializers
from .models import Job, JobCategory, SavedJob
from apps.profiles.serializers import SkillSerializer

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'

class JobListSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(source='recruiter.get_full_name', read_only=True)
    company_name = serializers.CharField(source='recruiter.recruiter_profile.company_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    skills = SkillSerializer(source='skills_required', many=True, read_only=True)
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'recruiter_name', 'company_name', 'category_name',
            'job_type', 'experience_level', 'location', 'is_remote',
            'salary_min', 'salary_max', 'salary_currency', 'status',
            'views_count', 'applications_count', 'skills', 'is_saved',
            'created_at', 'expires_at'
        ]
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedJob.objects.filter(user=request.user, job=obj).exists()
        return False

class JobDetailSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(source='recruiter.get_full_name', read_only=True)
    company_name = serializers.CharField(source='recruiter.recruiter_profile.company_name', read_only=True)
    company_logo = serializers.ImageField(source='recruiter.recruiter_profile.company_logo', read_only=True)
    category = JobCategorySerializer(read_only=True)
    skills_required = SkillSerializer(many=True, read_only=True)
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = '__all__'
    
    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedJob.objects.filter(user=request.user, job=obj).exists()
        return False

class JobCreateUpdateSerializer(serializers.ModelSerializer):
    skills_required_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    
    class Meta:
        model = Job
        exclude = ['recruiter', 'views_count', 'applications_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        skills_ids = validated_data.pop('skills_required_ids', [])
        job = Job.objects.create(**validated_data)
        if skills_ids:
            job.skills_required.set(skills_ids)
        return job
    
    def update(self, instance, validated_data):
        skills_ids = validated_data.pop('skills_required_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if skills_ids is not None:
            instance.skills_required.set(skills_ids)
        return instance

class SavedJobSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    
    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'saved_at']