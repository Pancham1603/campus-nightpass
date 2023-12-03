python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py crontab add
python manage.py crontab run
python manage.py crontab add
gunicorn -b 0.0.0.0:4376 core.wsgi:application