#!/bin/bash
python manage.py makemigrations
python manage.py makemigrations shortener
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
