from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('technical', 'Technical Assessment'),
        ('offer', 'Offer Extended'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='applications/resumes/%Y/%m/', blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notice_period = models.PositiveIntegerField(help_text='In days', default=30)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    status_notes = models.TextField(blank=True)
    
    recruiter_notes = models.TextField(blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.applicant.email} - {self.job.title}"

class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Application Status Histories'