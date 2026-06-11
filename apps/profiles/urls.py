from django.urls import path
from .views import (
    CandidateProfileView, SkillListView, AddSkillView,
    ExperienceView, EducationView
)

urlpatterns = [
    path('candidate/', CandidateProfileView.as_view(), name='candidate-profile'),
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('skills/add/', AddSkillView.as_view(), name='add-skill'),
    path('experience/', ExperienceView.as_view(), name='experience'),
    path('experience/<int:pk>/', ExperienceView.as_view(), name='experience-detail'),
    path('education/', EducationView.as_view(), name='education'),
    path('education/<int:pk>/', EducationView.as_view(), name='education-detail'),
]