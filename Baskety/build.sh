#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

mkdir -p staticfiles
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser automatically if it doesn't exist
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baskety_core.settings')
import django
django.setup()
from accounts.models import User
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@baskety.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username=username, email=email, password=password, role='admin')
    print(f'Superuser {username} created successfully')
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.role = 'admin'
    user.save()
    print(f'Superuser {username} updated successfully')
"
