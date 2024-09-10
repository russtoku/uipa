#!/bin/ash

yarn install
yarn build
yarn serve dev &

# To initialise the database:
/root/.local/bin/poetry run ./manage.py migrate --skip-checks

if [[ -z "${INITIALIZE_DB}" ]];
then
  # Create and populate search index
  /root/.local/bin/poetry run ./manage.py search_index --create
  /root/.local/bin/poetry run ./manage.py search_index --populate
fi

if [[ -z "${LOAD_DATA}" ]];
then
  echo "Load the seed data..."
  /root/.local/bin/poetry run ./manage.py loaddata uipa_org/fixtures/*
fi

/root/.local/bin/poetry run /bin/ash /srv/django/run-django.sh