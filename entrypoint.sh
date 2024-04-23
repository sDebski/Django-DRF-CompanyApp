#!/bin/sh

# apply migrations
python3 manage.py migrate 

python3 manage.py collectstatic --no-input
# populate database and crete admin user
python3 manage.py populate_database 

# run server
python3 manage.py runserver 0.0.0.0:8000