python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --clear
yes
gunicorn -b 0.0.0.0:4376 core.wsgi:application