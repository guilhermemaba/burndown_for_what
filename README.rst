=============================
Burndown for what
=============================

.. image:: https://badge.fury.io/py/burndown_for_what.png
    :target: https://badge.fury.io/py/burndown_for_what

.. image:: https://travis-ci.org/guilhermemaba/burndown_for_what.png?branch=master
    :target: https://travis-ci.org/guilhermemaba/burndown_for_what

Simple django application for generate burndown graphics.

Documentation
-------------

The full documentation is at https://burndown_for_what.readthedocs.org.

Quickstart
----------

Install burndown_for_what::

    pip install burndown_for_what

In your django project, configure **settings.py**::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'burndown_for_what',
        'rest_framework',
    )
    GITHUB_DATA = {
        'login': 'your@login.com',
        'password': 'your_token',
        'user': 'org_or_user',
        'repo': 'repository',
    }

And then yours **urls.py**::

    from django.conf.urls import include, url
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^burndown/', include('burndown_for_what.urls')),
    ]

You need to creating a sprint and their *dailys*, when saving the sprint, will be sought all github data.

.. image:: https://cloud.githubusercontent.com/assets/6231505/14302236/211a8ef6-fb75-11e5-9299-016c362aff57.png

That's it, run the project server::

    (virtualenv)guilhermemaba test_scrum # ./manage.py runserver
    Performing system checks...

    System check identified no issues (0 silenced).
    October 26, 2015 - 22:25:16
    Django version 1.8.5, using settings 'test_scrum.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

You can access http://127.0.0.1:8000/burndown/sprint/1/

.. image:: https://cloud.githubusercontent.com/assets/6231505/14302015/cb503f40-fb72-11e5-9019-e1afc1e798da.png

Features
--------

* TODO

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
*  django-rest-framework
