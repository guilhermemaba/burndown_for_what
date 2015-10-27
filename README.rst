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

In you django project, configure **settings.py**::

    INSTALLED_APPS = (
        'grappelli',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'burndown_for_what',
    )

And then yours **urls.py**::

    from django.conf.urls import include, url
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^grappelli/', include('grappelli.urls')),
        url(r'^burndown/', include('burndown_for_what.urls')),
    ]

If you prefer, you can import the sample fixtures::

    /manage.py loaddata initial_data --app=burndown_for_what

That's it, run the project server::

    (virtualenv)guilhermemaba test_scrum # ./manage.py runserver
    Performing system checks...

    System check identified no issues (0 silenced).
    October 26, 2015 - 22:25:16
    Django version 1.8.5, using settings 'test_scrum.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

You can access *127.0.0.1:8000/burndown/sprint/1/*::

.. image:: https://cloud.githubusercontent.com/assets/6231505/10746691/aba0e00e-7c34-11e5-9c1f-88263b9f3dd8.png


Features
--------

* TODO

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
