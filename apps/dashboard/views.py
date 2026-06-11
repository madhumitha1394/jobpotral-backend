from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from calendar import month_name
from apps.jobs.models import Job
from apps.applications.models import JobApplication
from apps.accounts.models import User
from .serializers import AdminDashboardSerializer, RecruiterDashboardSerializer

class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.user_type != 'admin' and not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=403)
        
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        
        # Stats
        stats = {
            'total_jobs': Job.objects.count(),
            'total_applications': JobApplication.objects.count(),
            'total_candidates': User.objects.filter(user_type='candidate').count(),
            'total_recruiters': User.objects.filter(user_type='recruiter').count(),
            'pending_applications': JobApplication.objects.filter(status='applied').count(),
            'hired_count': JobApplication.objects.filter(status='hired').count(),
            'rejected_count': JobApplication.objects.filter(status='rejected').count(),
            'active_jobs': Job.objects.filter(status='published', expires_at__gt=now).count(),
        }
        
        # Monthly stats for current year
        monthly_stats = []
        for month in range(1, 13):
            month_jobs = Job.objects.filter(
                created_at__year=now.year,
                created_at__month=month
            ).count()
            month_apps = JobApplication.objects.filter(
                applied_at__year=now.year,
                applied_at__month=month
            ).count()
            month_hires = JobApplication.objects.filter(
                status='hired',
                updated_at__year=now.year,
                updated_at__month=month
            ).count()
            
            monthly_stats.append({
                'month': month_name[month][:3],
                'jobs_posted': month_jobs,
                'applications_received': month_apps,
                'hires': month_hires
            })
        
        # Recent activities
        recent_jobs = Job.objects.select_related('recruiter').order_by('-created_at')[:5]
        recent_apps = JobApplication.objects.select_related('applicant', 'job').order_by('-applied_at')[:5]
        
        activities = []
        for job in recent_jobs:
            activities.append({
                'id': job.id,
                'type': 'job_posted',
                'description': f"New job posted: {job.title}",
                'created_at': job.created_at,
                'user': job.recruiter.get_full_name()
            })
        
        for app in recent_apps:
            activities.append({
                'id': app.id,
                'type': 'application',
                'description': f"Applied for {app.job.title}",
                'created_at': app.applied_at,
                'user': app.applicant.get_full_name()
            })
        
        activities.sort(key=lambda x: x['created_at'], reverse=True)
        activities = activities[:10]
        
        data = {
            'stats': stats,
            'monthly_stats': monthly_stats,
            'recent_activities': activities
        }
        
        serializer = AdminDashboardSerializer(data)
        return Response(serializer.data)

class RecruiterDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.user_type != 'recruiter':
            return Response({'detail': 'Permission denied'}, status=403)
        
        now = timezone.now()
        recruiter = request.user
        
        total_jobs = Job.objects.filter(recruiter=recruiter).count()
        active_jobs = Job.objects.filter(recruiter=recruiter, status='published').count()
        total_apps = JobApplication.objects.filter(job__recruiter=recruiter).count()
        new_apps = JobApplication.objects.filter(
            job__recruiter=recruiter,
            status='applied',
            applied_at__gte=now - timedelta(days=7)
        ).count()
        interviews = JobApplication.objects.filter(
            job__recruiter=recruiter,
            status='interview'
        ).count()
        hires = JobApplication.objects.filter(
            job__recruiter=recruiter,
            status='hired'
        ).count()
        
        monthly_stats = []
        for month in range(1, 13):
            month_apps = JobApplication.objects.filter(
                job__recruiter=recruiter,
                applied_at__year=now.year,
                applied_at__month=month
            ).count()
            month_hires = JobApplication.objects.filter(
                job__recruiter=recruiter,
                status='hired',
                updated_at__year=now.year,
                updated_at__month=month
            ).count()
            
            monthly_stats.append({
                'month': month_name[month][:3],
                'jobs_posted': Job.objects.filter(
                    recruiter=recruiter,
                    created_at__year=now.year,
                    created_at__month=month
                ).count(),
                'applications_received': month_apps,
                'hires': month_hires
            })
        
        data = {
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'total_applications': total_apps,
            'new_applications': new_apps,
            'interviews_scheduled': interviews,
            'hires': hires,
            'monthly_stats': monthly_stats,
            'recruiter': recruiter
        }
        
        serializer = RecruiterDashboardSerializer(data)
        return Response(serializer.data)

class UserManagementView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=403)
        
        users = User.objects.all().values(
            'id', 'email', 'first_name', 'last_name', 'user_type',
            'is_active', 'is_verified', 'created_at'
        ).order_by('-created_at')
        
        return Response(list(users))
    
    def patch(self, request, user_id):
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=403)
        
        user = User.objects.get(id=user_id)
        user.is_active = request.data.get('is_active', user.is_active)
        user.is_verified = request.data.get('is_verified', user.is_verified)
        user.save()
        
        return Response({'status': 'updated'})

class RecruiterApprovalView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=403)
        
        from apps.accounts.models import RecruiterProfile
        recruiters = RecruiterProfile.objects.filter(is_approved=False).select_related('user')
        
        return Response([{
            'id': r.id,
            'company_name': r.company_name,
            'user_email': r.user.email,
            'user_name': r.user.get_full_name(),
            'industry': r.industry,
            'location': r.location,
            'created_at': r.user.created_at
        } for r in recruiters])
    
    def post(self, request, recruiter_id):
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=403)
        
        from apps.accounts.models import RecruiterProfile
        profile = RecruiterProfile.objects.get(id=recruiter_id)
        profile.is_approved = request.data.get('approved', True)
        profile.save()
        
        return Response({'status': 'approved' if profile.is_approved else 'rejected'})