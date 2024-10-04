#!/bin/ash

yarn install
yarn build
yarn serve dev &


if [[ "${INITIALIZE_DB}" == "y" ]] || [[ "${INITIALIZE_DB}" == "Y" ]];
then
  echo "Initializing database"
  # To initialise the database:
  /root/.local/bin/poetry run ./manage.py migrate --skip-checks

  # Create and populate search index
  echo "Creating search indices..."
  /root/.local/bin/poetry run ./manage.py search_index --create
  /root/.local/bin/poetry run ./manage.py search_index --populate
else
  echo "Skipping database initialization and creation of search indices"
fi

if [[ "${LOAD_DATA}" == "y" ]] || [[ "${LOAD_DATA}" == "Y" ]];
then
  echo "Load the seed data..."
  /root/.local/bin/poetry run ./manage.py loaddata uipa_org/fixtures/*
else
  echo "Skipping seed data load"
fi

export DEBUG
/root/.local/bin/poetry run /bin/ash /srv/django/run-django.sh