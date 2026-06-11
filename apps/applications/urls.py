from django.urls import path
from .views import (
    ApplyForJobView, MyApplicationsView, ApplicationDetailView,
    WithdrawApplicationView, JobApplicationsView,
    UpdateApplicationStatusView, DownloadResumeView
)

urlpatterns = [
    path('apply/<int:job_id>/', ApplyForJobView.as_view(), name='apply-job'),
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('<int:pk>/withdraw/', WithdrawApplicationView.as_view(), name='withdraw-application'),
    path('job/<int:job_id>/applications/', JobApplicationsView.as_view(), name='job-applications'),
    path('<int:pk>/update-status/', UpdateApplicationStatusView.as_view(), name='update-status'),
    path('<int:pk>/download-resume/', DownloadResumeView.as_view(), name='download-resume'),
]