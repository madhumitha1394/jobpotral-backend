from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Job, JobCategory, SavedJob
from .serializers import (
    JobListSerializer, JobDetailSerializer, JobCreateUpdateSerializer,
    JobCategorySerializer, SavedJobSerializer
)
from .filters import JobFilter

class JobCategoryListView(generics.ListAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

class JobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'requirements', 'location']
    ordering_fields = ['created_at', 'salary_min', 'salary_max', 'views_count']
    
    def get_queryset(self):
        return Job.objects.filter(status='published', expires_at__gt=timezone.now())
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_object(self):
        obj = super().get_object()
        if obj.status == 'published':
            obj.views_count += 1
            obj.save(update_fields=['views_count'])
        return obj

class RecruiterJobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)

class JobCreateView(generics.CreateAPIView):
    serializer_class = JobCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'recruiter':
            raise permissions.PermissionDenied("Only recruiters can post jobs")
        serializer.save(recruiter=self.request.user)

class JobUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)

class ToggleJobStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk):
        job = get_object_or_404(Job, pk=pk, recruiter=request.user)
        if job.status == 'published':
            job.status = 'closed'
        else:
            job.status = 'published'
        job.save()
        return Response({'status': job.status})

class SavedJobListView(generics.ListAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)

class ToggleSaveJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        saved_job, created = SavedJob.objects.get_or_create(
            user=request.user, job=job
        )
        if not created:
            saved_job.delete()
            return Response({'saved': False, 'message': 'Job removed from saved'})
        return Response({'saved': True, 'message': 'Job saved successfully'})