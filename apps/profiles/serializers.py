from rest_framework import serializers
from .models import CandidateProfile, Skill, CandidateSkill, Experience, Education

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class CandidateSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), source='skill', write_only=True
    )
    
    class Meta:
        model = CandidateSkill
        fields = ['id', 'skill', 'skill_id', 'proficiency', 'years_experience']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ['candidate']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ['candidate']

class CandidateProfileSerializer(serializers.ModelSerializer):
    skills = CandidateSkillSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = CandidateProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class CandidateProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        exclude = ['user', 'created_at', 'updated_at']