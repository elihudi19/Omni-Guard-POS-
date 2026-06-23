#!/usr/bin/env bash
# Render runs this on every deploy
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser from env vars if not already created
python manage.py shell -c "
from backend.users.models import User
import os
u = os.environ.get('DJANGO_SUPERUSER_USERNAME','admin')
e = os.environ.get('DJANGO_SUPERUSER_EMAIL','admin@omniguard.app')
p = os.environ.get('DJANGO_SUPERUSER_PASSWORD','changeme123')
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, e, p, role='admin')
    print(f'Superuser {u} created.')
else:
    print(f'Superuser {u} already exists.')
"
