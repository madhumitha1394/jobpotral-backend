import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    max_salary = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    category = django_filters.NumberFilter(field_name='category__id')
    is_remote = django_filters.BooleanFilter(field_name='is_remote')
    
    class Meta:
        model = Job
        fields = ['job_type', 'experience_level', 'location', 'category', 'is_remote']