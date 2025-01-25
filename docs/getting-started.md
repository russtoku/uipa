# Getting Started

This is for developers and others who want to contribute to improve the project.

## Prerequisite libraries and programs

 - Python 3.8 in a virtual environment (python -m venv venv3)
    - **NOTE:** Use a pip version less than 24 with Python 3.8.
 - libmagic (yum install libmagic, apt-get install libmagic, etc.)
 - PostgreSQL - psycopg2 needs the libraries locally.
 - Docker
    - Desktop (Mac or Windows) - See [Overview of Docker Desktop](https://docs.docker.com/desktop/)
    - Engine (Linux) - See [Docker Engine overview](https://docs.docker.com/engine/)

## Set up

Clone this repo and change into the directory that the repo was cloned to.

Set DOCKER_DEFAULT_PLATFORM to linux/amd64 on macOS and Windows:

    export DOCKER_DEFAULT_PLATFORM=linux/amd64

Start a PostgreSQL database and an Elasticsearch server in docker containers using:

    docker compose up -d

After activating your Python 3.8 virtualenv, run the first time after cloning the repo:

```
$ pip install -r requirements.txt
$ python manage.py migrate  --noinput
$ python manage.py loaddata uipa_org/fixtures/*
$ python manage.py compress
```

## Run the dev server

Run this to start the dev server:

```
$ python manage.py runserver
```

## Visit the dev website

At this point, visit http://127.0.0.1:8000/ in your browser and you should see the home page for
uipa.org.

The user, `admin` (admin@uipa.org) was created from a fixture file and its password is
*testing*. Two regular users, `lani` (lani@uipa.org) and `joe` (joe@uipa.org), were also created and
their passwords are the same.

To sign into the dev website, use the email address and password.

## Visit the dev Admin website

Log on to the Admin site at http://127.0.0.1:8000/uipa-admin/. You can create or modify flatpages
there.

## Using the dev website

### Searching for public agencies or requests

UIPA uses an Elasticsearch server to handle indexing public agencies and
requests that have been submitted. A Docker compose file is provided so
developers don't have to manually install an Elasticsearch server.

The indexes are automatically updated when changes are made in UIPA.

### Making a request for information

Click on the *Make a Request* button at the top of the home page to start the process of making
a request for information.

You'll need to select the public agency that you wish to request information from and indicate that
the request is for *public* information and not *personal* information. The uipa.org website is not
for requesting your *personal* information from local (county or state) government agencies.

## Creating page content for the About, Help, Terms of Use, and Privacy Statement links

Django Flat Pages are used to create these pages. They are "flat" HTML content
stored in the database. For details, see [The flatpages
app](https://docs.djangoproject.com/es/1.9/ref/contrib/flatpages/)
documentation.

To create these pages initially, we:

- Create the pages using the Admin website at http://127.0.0.1:8000/uipa-admin/. Click on the *Flat
pages* link and add the pages.
- Dump the database in JSON format (see below).
- Edit the dump file, `<db-dump>.json`.
- Copy the section of JSON data for the model, `flatpages.flatpage` (see below).
- Put the JSON data in a file under the uipa_org/fixtures directory named `flatpages.flatpage.json`.

### Loading the page data

Once the page data files have been created under the fixtures directory, they can be loaded whenever
a new instance of uipa.org is created. This is done by loading the page data files using this
command:

```
python manage.py loaddata <page>
```

where `<page>` is the name of the page data file without the `.json` extension. Multiple pages can
be loaded at the same time.

### Dumping the database

Dumping the database in JSON format is done using the command:

```
python manage.py dumpdata --indent 4 > db-dump.json
```

### Page data in JSON format

Here's an example of the page data in JSON format for the About page in the
`fixtures/about-page.json`:

```
[
    {
        "fields": {
            "content": "<p>UIPA.org is the place where you can request information from your State of Hawaii government.</p>\r\n\r\n<p>UIPA stands for Uniform Information Practices Act and is the law covered by HRS Chapter 92F. It requires open access to government records. More information about the law can be seen at the State of Hawaii Office of Information Practices (OIP) website at <a href=\"http://oip.hawaii.gov/laws-rules-opinions/uipa/\">http://oip.hawaii.gov/laws-rules-opinions/uipa/</a>.</p>\r\n<p>You'll probably want to start with the <a href=\"http://oip.hawaii.gov/basic-qa-on-access-to-government-records/\">Basic Q&A on Access to Government Records</a> page where you can find out:</p>\r\n<ul><li>What types of records are public,</li><li>Who can request a record,</li><li>What government records are restricted or closed by law</li></ul></p>",
            "enable_comments": false,
            "registration_required": false,
            "sites": [
                1
            ],
            "template_name": "help/page.html",
            "title": "About UIPA.org",
            "url": "/help/about/"
        },
        "model": "flatpages.flatpage",
        "pk": 1
    }
]
```

## Froide documentation

uipa.org is built from the Froide website and Froide Theme open source software. For reference, see
[http://froide.readthedocs.org/en/latest/gettingstarted/](http://froide.readthedocs.org/en/latest/gettingstarted/).

For details about working with Froide Themes, see [Theming
Froide](http://froide.readthedocs.org/en/latest/theming/).

## Running UIPA on Heroku

> This is out-dated and will be changed as future deployment procedures are developed.

There is a complete guide of how to set up Froide on Heroku at
http://froide.readthedocs.org/en/latest/herokudeployment/. For UIPA, you'll
need to interpolate a bit to run on a similar hardware platform provider or your
own local machines (test, staging, production, etc.).
