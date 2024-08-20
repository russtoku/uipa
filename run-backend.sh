#!/bin/ash

export GDAL_LIBRARY_PATH='/usr/lib/libgdal.so.34'
export GEOS_LIBRARY_PATH='/usr/lib/libgeos_c.so.1'

#git clone https://github.com/codewithaloha/froide.git
#yarn link
yarn install
yarn build
yarn serve dev &

# hack until we get the froide setup build working (i.e. include templates)
echo "STARTING DB"
# To initialise the database:
/root/.local/bin/poetry run ./manage.py migrate --skip-checks
# Create a superuser
/root/.local/bin/poetry run ./manage.py createsuperuser
# Create and populate search index
/root/.local/bin/poetry run ./manage.py search_index --create
/root/.local/bin/poetry run ./manage.py search_index --populate

#/root/.local/bin/poetry run ./manage.py diffsettings --all
/root/.local/bin/poetry run /bin/ash /srv/django/run-django.sh