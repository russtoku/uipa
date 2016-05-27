#!/usr/bin/env bash

rm -f './dev.db' 2>/dev/null && python manage.py migrate && python manage.py createsuperuser --username uipa --email admin@uipa.org && python manage.py loaddata uipa_org/fixtures/* && python manage.py import_csv 'data/2016-05-27-Hawaii_UIPA_Public_Bodies_All.csv'
