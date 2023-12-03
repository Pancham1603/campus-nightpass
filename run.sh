python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
service cron start
tail -f /var/log/cron.log
gunicorn -b 0.0.0.0:4376 core.wsgi:application