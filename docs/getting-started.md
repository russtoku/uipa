# Getting Started

This is for developers and others who want to contribute to improve the project.

We're currently using Python 3.12 and Django 5.2.

## Prerequisite libraries and programs

 - Python 3.12 in a virtual environment
    - **NOTE:** Use [uv](https://docs.astral.sh/uv/) to create a virtual environment and install
      dependencies.
 - libmagic - An implementation of file command.
    - Use: `yum install libmagic`, `apt-get install libmagic`, `brew install libmagic`, etc.
 - PostgreSQL
    - psycopg2 needs the client libraries to be installed locally so you'll need to install
      PostgreSQL. The bundle includes the server and client.
 - Docker
    - Desktop (Mac or Windows) - See [Overview of Docker Desktop](https://docs.docker.com/desktop/)
    - Engine (Linux) - See [Docker Engine overview](https://docs.docker.com/engine/)

## Set up

Clone this repo and change into the directory that the repo was cloned to.

If you have trouble with running the Docker images on macOS running on Apple Silicon (e.g., M3
Macbook), you may need to do this:

> Set DOCKER_DEFAULT_PLATFORM to linux/amd64 on macOS and Windows:
>
> $ export DOCKER_DEFAULT_PLATFORM=linux/amd64

Start a PostgreSQL database and an Elasticsearch server in Docker containers using:

```console
$ docker compose up -d
```

*NOTE: A test email service for sending and receiving messages is also started up but you can ignore
it for now.*

## Set up Python virutal environment

We use `uv` to manage our Python virtual environment. Install it following the
[installation](https://docs.astral.sh/uv/getting-started/installation/) instructions.

### Create a Python virtual environment

```console
$ uv venv -p 3.12

```

The virutal environment is created in the current directory in a subdirectory named, `.venv`.

### Install dependencies in the virtual environment

```console
$ uv pip install -r pyproject.toml
```

*CAUTION: Don't use `uv sync --frozen` yet.*


### Apply patches to these dependencies:

These patches fix problems that prevent the website from running.

1. Patch widgets.py in django-floppyforms module.
    - Error message in console window.
        ``` console
        File "/Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa/.venv/lib/python3.12/site-packages/floppyforms/__init__.py", line 5, in <module>
            from .fields import *
        File "/Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa/.venv/lib/python3.12/site-packages/floppyforms/fields.py", line 5, in <module>
            from .widgets import (TextInput, HiddenInput, CheckboxInput, Select,
        File "/Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa/.venv/lib/python3.12/site-packages/floppyforms/widgets.py", line 10, in <module>
            from django.utils import datetime_safe, formats
        ImportError: cannot import name 'datetime_safe' from 'django.utils' (/Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa/.venv/lib/python3.12/site-packages/django/utils/__init__.py)
        ```

     - Fix is not to use datetime_safe from django.utils.
        ``` console
        $ patch -b < floppyforms-widgets.patch
        patching file '.venv/lib/python3.12/site-packages/floppyforms/widgets.py'

        $ ls -l .venv/lib/python3.12/site-packages/floppyforms/widge*
        -rw-r--r--@ 1 russ  staff  28916 Apr 24 09:38 .venv/lib/python3.12/site-packages/floppyforms/widgets.py
        -rw-r--r--@ 1 russ  staff  29103 Jan 24 21:52 .venv/lib/python3.12/site-packages/floppyforms/widgets.py.orig
        ```

2. Patch boundfield.py in django forms module.
    - Error message in browser window.
        ``` console
        TypeError at /account/login/
        AgreeCheckboxInput.render() got an unexpected keyword argument 'renderer'

        Request Method:        GET
        Request URL:           http://127.0.0.1:8000/account/login/
        Django Version:        5.2
        Exception Type:        TypeError
        Exception Value:       AgreeCheckboxInput.render() got an unexpected keyword argument 'renderer'
        Exception Location:    /Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa/.venv/lib/python3.12/site-packages/django/forms/boundfield.py, line 108, in as_widget
        Raised during:         froide.account.views.login
        Python Executable:     /Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa/.venv/bin/python
        Python Version:        3.12.8
        Python Path:           ['/Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa',
                                '/Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa',
                                '/Users/russ/.local/share/uv/python/cpython-3.12.8-macos-aarch64-none/lib/python312.zip',
                                '/Users/russ/.local/share/uv/python/cpython-3.12.8-macos-aarch64-none/lib/python3.12',
                                '/Users/russ/.local/share/uv/python/cpython-3.12.8-macos-aarch64-none/lib/python3.12/lib-dynload',
                                '/Users/russ/Projects/Code_With_Aloha/Code_for_Hawaii/Update_orig/uipa/.venv/lib/python3.12/site-packages']
        Server time:           Thu, 24 Apr 2025 08:09:11 -1000
        ```

    - Fix is not to pass "renderer=self.form.renderer" to `widget.render()` in as_widget function of
      BoundField class.
        ``` console
        $ patch -b < djano-form-boundfield.patch
        patching file '.venv/lib/python3.12/site-packages/django/forms/boundfield.py'

        $ ls -l .venv/lib/python3.12/site-packages/django/forms/bound*
        -rw-r--r--@ 1 russ  staff  13272 Apr 24 09:38 .venv/lib/python3.12/site-packages/django/forms/boundfield.py
        -rw-r--r--@ 1 russ  staff  13271 Apr 15 08:05 .venv/lib/python3.12/site-packages/django/forms/boundfield.py.orig
        ```


3. **Optional:** Patch elasticsearch client module.
    - Warning message in console window. Appears when the virutal environment is initially created.
        ``` console
        .venv/lib/python3.12/site-packages/elasticsearch/client/__init__.py:463: SyntaxWarning: invalid escape sequence '\_'
        ```

    - Fix is to use raw string for docstring.
        ``` console
        $ patch -b < elasticsearch-client.patch
        patching file '.venv/lib/python3.12/site-packages/elasticsearch/client/__init__.py'

        $ ls -l .venv/lib/python3.12/site-packages/elasticsearch/client/__init*
        -rw-r--r--@ 1 russ  staff  71850 Apr 24 09:38 .venv/lib/python3.12/site-packages/elasticsearch/client/__init__.py
        -rw-r--r--@ 1 russ  staff  71849 Apr 15 08:54 .venv/lib/python3.12/site-packages/elasticsearch/client/__init__.py.orig
        ```


### Trouble when installing dependencies

If you are running on `macOS` and have installed `Postgres` using homebrew, then you may need to
tell the C linker where to find the ssl and/or other libraries when compiling Python packages that
have binary libraries that need to be compiled like `psycopg2`.

```console
$ LDFLAGS="-L /opt/homebrew/lib" uv sync --frozen
```

For other OSes, you may need to do the same if you see linker errors like:

```console
      In file included from ./psycopg/psycopg.h:38:
      ./psycopg/config.h:82:13: warning: unused function 'Dprintf' [-Wunused-function]
         82 | static void Dprintf(const char *fmt, ...) {}
            |             ^~~~~~~
      1 warning generated.
      ld: library 'ssl' not found
      clang: error: linker command failed with exit code 1 (use -v to see invocation)
      error: command '/usr/bin/cc' failed with exit code 1
```


### Activate the virtual environment

To activate the virtual environment, source the activate script from the virtual environment.

```console
$ source .venv/bin/activate
```

Verify that the version of Python is correct.

```console
$ python -V
Python 3.12.8
```

## Load the seed data

In another terminal window, start up the database server and search engine using:

```console
$ docker-compose up
```

In another terminal window, load the seed data by running:

```console
$ python manage.py loaddata uipa_org/fixtures/*
```

## Compress the web assets

Only the first time after cloning the repo, run this command to compress the web assets.

```console
$ python manage.py compress
```

If you make changes to the CSS styles or JavaScript files, you will need to run the above command
again.

If you recreate the database volume in Docker, you may need to run the above command again.


## Run the dev server

Run this to start the dev server:

```console
$ python manage.py runserver
```

## Visit the dev website

Visit http://127.0.0.1:8000/ in your browser and you should see the home page for uipa.org.

The superuser, `admin` (admin@uipa.org) was created from a fixture file and its password is
*testing*.

Two regular users, `lani` (lani@uipa.org) and `joe` (joe@uipa.org), were also created and their
passwords are the same.

To sign into the dev website, use the email address and password.

## Visit the dev Admin website

Log on to the Admin site at http://127.0.0.1:8000/uipa-admin/.

On the Admin site, you can create or modify flatpages. You can also view or change other data.

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

```console
$ python manage.py loaddata <page>
```

where `<page>` is the name of the page data file without the `.json` extension. Multiple pages can
be loaded at the same time.

### Dumping the database

Dumping the database in JSON format is done using the command:

```console
$ python manage.py dumpdata --indent 4 > db-dump.json
```

### Page data in JSON format

Here's an example of the page data in JSON format for the About page in the
`fixtures/about-page.json`:

```json
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

The Froide source has been included in the uipa.org source so that it is no longer a dependency that
needs to be installed from the master branch of Code With Aloha's fork of Froide. See the [Roadmap
for upgrade in-place](Roadmap.md).
