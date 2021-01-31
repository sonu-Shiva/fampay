#!/bin/bash
set -e
cmd="$@"

# if [ -z "$REDIS_URL" ]; then
#     # export REDIS_URL=redis://redis:6379
#     export REDIS_URL=$CELERY_BROKER_URL
# fi

# export CELERY_BROKER_URL=$REDIS_URL/2

# if [ -z "$DJANGO_CACHE_LOCATION" ]; then
#     export DJANGO_CACHE_LOCATION=$REDIS_URL/1
# fi

if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL=postgres://postgres:postgres@postgres:5432/postgres
fi

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect("$DATABASE_URL")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."


if [ -z $cmd ]; then
  python /app/manage.py collectstatic --noinput
  python /app/manage.py migrate --noinput

  python manage.py runserver 0:8000
else
  >&2 echo "Running command passed (by the compose file)"
  exec $cmd
fi

# tail -f /dev/null
# python manage.py runserver 0:8000
