#!/bin/ash


if [[ -z "${DEBUG}" ]];
then
  python ./manage.py diffsettings --all
fi

python ./manage.py runserver  0.0.0.0:8000