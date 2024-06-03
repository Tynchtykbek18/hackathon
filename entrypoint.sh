#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input

celery -A config worker -l info --without-gossip --without-mingle --without-heartbeat &
exec /bin/sh -c "gunicorn --bind :8000 config.wsgi:application"

chmod +x entrypoint.sh