
#! /bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt 

echo "Applying migrations and collecting static files..."
python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate