from django.urls import path
from .views import (
    JobCategoryListView, JobListView, JobDetailView,
    RecruiterJobListView, JobCreateView, JobUpdateDeleteView,
    ToggleJobStatusView, SavedJobListView, ToggleSaveJobView
)

urlpatterns = [
    path('categories/', JobCategoryListView.as_view(), name='job-categories'),
    path('', JobListView.as_view(), name='job-list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('recruiter/my-jobs/', RecruiterJobListView.as_view(), name='recruiter-jobs'),
    path('recruiter/create/', JobCreateView.as_view(), name='job-create'),
    path('recruiter/<int:pk>/', JobUpdateDeleteView.as_view(), name='job-update-delete'),
    path('recruiter/<int:pk>/toggle-status/', ToggleJobStatusView.as_view(), name='toggle-status'),
    path('saved/', SavedJobListView.as_view(), name='saved-jobs'),
    path('<int:pk>/save/', ToggleSaveJobView.as_view(), name='toggle-save'),
]