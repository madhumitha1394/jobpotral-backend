import os
import sys

print("Python:", sys.executable)
print("CWD:", os.getcwd())
print()

files_to_check = [
    'manage.py',
    'requirements.txt',
    'backend/settings.py',
    'backend/urls.py',
    'apps/__init__.py',
    'apps/accounts/models.py',
    'apps/profiles/models.py',
    'apps/jobs/models.py',
    'apps/applications/models.py',
    'apps/dashboard/views.py',
]

for f in files_to_check:
    exists = os.path.exists(f)
    size = os.path.getsize(f) if exists else 0
    status = "OK" if exists and size > 0 else "MISSING/EMPTY"
    print(f"{status}: {f} ({size} bytes)")

print()
try:
    import django
    print(f"Django: {django.__version__}")
except ImportError:
    print("Django: NOT INSTALLED")

try:
    import rest_framework
    print(f"DRF: {rest_framework.__version__}")
except ImportError:
    print("DRF: NOT INSTALLED")

try:
    import corsheaders
    print("django-cors-headers: INSTALLED")
except ImportError:
    print("django-cors-headers: NOT INSTALLED")