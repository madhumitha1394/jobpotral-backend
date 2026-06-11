from django.urls import path
from .views import (
    AdminDashboardView, RecruiterDashboardView,
    UserManagementView, RecruiterApprovalView
)

urlpatterns = [
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('recruiter/', RecruiterDashboardView.as_view(), name='recruiter-dashboard'),
    path('users/', UserManagementView.as_view(), name='user-management'),
    path('users/<int:user_id>/', UserManagementView.as_view(), name='user-update'),
    path('recruiters/pending/', RecruiterApprovalView.as_view(), name='pending-recruiters'),
    path('recruiters/<int:recruiter_id>/approve/', RecruiterApprovalView.as_view(), name='approve-recruiter'),
]