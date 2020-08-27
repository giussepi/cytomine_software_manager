#!/bin/bash
#
# Creates the super user, if necessary
# Starts supervisor
#

cd /myapp/cyto_soft_mgr

wait-for $POSTGRES_CONTAINER:$POSTGRES_DB_PORT -- python3 manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DJANGO_ADMIN_USER', '$DJANGO_ADMIN_EMAIL', '$DJANGO_ADMIN_PASS') if not User.objects.filter(is_superuser=True) else print('superuser already created')" | python3 manage.py shell

supervisord -c /etc/supervisor/supervisord.conf

exec "$@"
