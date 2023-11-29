python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn -b 0.0.0.0:4376 core.wsgi:application