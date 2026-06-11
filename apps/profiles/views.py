from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import CandidateProfile, Skill, CandidateSkill, Experience, Education
from .serializers import (
    CandidateProfileSerializer, CandidateProfileCreateUpdateSerializer,
    SkillSerializer, CandidateSkillSerializer, 
    ExperienceSerializer, EducationSerializer
)

class CandidateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            profile = request.user.candidate_profile
            serializer = CandidateProfileSerializer(profile)
            return Response(serializer.data)
        except CandidateProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=404)
    
    def post(self, request):
        if hasattr(request.user, 'candidate_profile'):
            return Response({'detail': 'Profile already exists'}, status=400)
        
        if request.user.user_type != 'candidate':
            return Response({'detail': 'Only candidates can create this profile'}, status=403)
        
        serializer = CandidateProfileCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(CandidateProfileSerializer(serializer.instance).data, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    
    def patch(self, request):
        try:
            profile = request.user.candidate_profile
            serializer = CandidateProfileCreateUpdateSerializer(
                profile, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(CandidateProfileSerializer(serializer.instance).data)
            return Response(serializer.errors, status=400)
        except CandidateProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=404)

class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

class AddSkillView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            profile = request.user.candidate_profile
        except CandidateProfile.DoesNotExist:
            return Response({'detail': 'Candidate profile not found'}, status=404)
        
        skill_id = request.data.get('skill_id')
        proficiency = request.data.get('proficiency', 1)
        years = request.data.get('years_experience', 0)
        
        skill = get_object_or_404(Skill, id=skill_id)
        candidate_skill, created = CandidateSkill.objects.get_or_create(
            candidate=profile, skill=skill,
            defaults={'proficiency': proficiency, 'years_experience': years}
        )
        
        if not created:
            candidate_skill.proficiency = proficiency
            candidate_skill.years_experience = years
            candidate_skill.save()
        
        return Response(CandidateSkillSerializer(candidate_skill).data)

class ExperienceView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            profile = request.user.candidate_profile
        except CandidateProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=404)
        
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(candidate=profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk, candidate__user=request.user)
        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk, candidate__user=request.user)
        experience.delete()
        return Response(status=204)

class EducationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            profile = request.user.candidate_profile
        except CandidateProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=404)
        
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(candidate=profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        education = get_object_or_404(Education, pk=pk, candidate__user=request.user)
        serializer = EducationSerializer(education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        education = get_object_or_404(Education, pk=pk, candidate__user=request.user)
        education.delete()
        return Response(status=204)