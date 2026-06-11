from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import JobApplication, ApplicationStatusHistory
from .serializers import (
    JobApplicationSerializer, JobApplicationCreateSerializer,
    UpdateStatusSerializer, ApplicationStatusHistorySerializer
)

class ApplyForJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, job_id):
        if request.user.user_type != 'candidate':
            return Response({'detail': 'Only candidates can apply'}, status=403)
        
        serializer = JobApplicationCreateSerializer(
            data=request.data,
            context={'request': request, 'job_id': job_id}
        )
        if serializer.is_valid():
            application = serializer.save(applicant=request.user, job_id=job_id)
            
            # Update job application count
            job = application.job
            job.applications_count += 1
            job.save(update_fields=['applications_count'])
            
            return Response(
                JobApplicationSerializer(application).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=400)

class MyApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)

class ApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)

class WithdrawApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        application = get_object_or_404(
            JobApplication, pk=pk, applicant=request.user
        )
        if application.status in ['hired', 'rejected']:
            return Response(
                {'detail': 'Cannot withdraw this application'},
                status=400
            )
        
        old_status = application.status
        application.status = 'withdrawn'
        application.save()
        
        ApplicationStatusHistory.objects.create(
            application=application,
            old_status=old_status,
            new_status='withdrawn',
            changed_by=request.user,
            notes='Withdrawn by applicant'
        )
        
        return Response({'status': 'withdrawn'})

# Recruiter Views
class JobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404('jobs.Job', pk=job_id, recruiter=self.request.user)
        return JobApplication.objects.filter(job=job)

class UpdateApplicationStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        
        # Check if user is the job recruiter
        if application.job.recruiter != request.user:
            return Response({'detail': 'Permission denied'}, status=403)
        
        serializer = UpdateStatusSerializer(data=request.data)
        if serializer.is_valid():
            old_status = application.status
            new_status = serializer.validated_data.get('status')
            
            application.status = new_status
            application.status_notes = serializer.validated_data.get('status_notes', '')
            if 'interview_date' in serializer.validated_data:
                application.interview_date = serializer.validated_data['interview_date']
            application.save()
            
            ApplicationStatusHistory.objects.create(
                application=application,
                old_status=old_status,
                new_status=new_status,
                changed_by=request.user,
                notes=serializer.validated_data.get('status_notes', '')
            )
            
            return Response(JobApplicationSerializer(application).data)
        return Response(serializer.errors, status=400)

class DownloadResumeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        
        if application.job.recruiter != request.user:
            return Response({'detail': 'Permission denied'}, status=403)
        
        if not application.resume:
            return Response({'detail': 'No resume uploaded'}, status=404)
        
        # Return resume file URL
        return Response({'resume_url': request.build_absolute_uri(application.resume.url)})