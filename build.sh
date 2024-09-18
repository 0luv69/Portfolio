#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files for Django
python manage.py collectstatic --noinput

# Run migrations (if necessary)
python manage.py migrate --noinput