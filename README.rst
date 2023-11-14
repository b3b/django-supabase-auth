==============================
Django Supabase authentication
==============================

.. start-badges
.. image:: https://img.shields.io/badge/stability-wip-lightgrey.svg
    :target: https://github.com/b3b/django-supabase-auth
    :alt: Stability
.. image:: https://img.shields.io/pypi/v/django-supabase-auth.svg
    :target: https://pypi.python.org/pypi/django-supabase-auth
    :alt: Latest version on PyPi
.. end-badges


Experimental project aimed at exploring the integration of Supabase with Django.

Disclaimer
==========

Please note that this repository is for experimental purposes only. It may contain incomplete or unstable code. Use it at your own risk.

Installation
============

You can install the latest released package version from PyPI using::

    pip install django-supabase-auth[database]

Usage
=====

Django project settings.py
--------------------------

Add `supa_auth` to INSTALLED_APPS::

    INSTALLED_APPS = [
        #  ... ,
        "rest_framework",
        "supa_auth",
    ]

Fill in your Supabase database settings.

Retrieve these values from the Supabase dashboard under Database Settings

https://supabase.com/dashboard/project/_/settings/database .

At a minimum, ensure "HOST" and "PASSWORD" are configured::

    DATABASES = {
        "default": {
            "ENGINE": "supa_auth",
            "HOST": "db.*.supabase.co",
            "PASSWORD": "...",
            "OPTIONS": {
                "sslmode": "require",
            },
        },
    }

The `supa_auth` engine automatically populates "NAME" and "USER" to default values ("postgres")::

Database migrations
-------------------

Apply migrations to initialize the database::

    python manage.py migrate

Checking Setup
--------------

You can verify the setup using the command-line database client::

    python manage.py dbshell

    postgres=> SELECT count(*) FROM users;
