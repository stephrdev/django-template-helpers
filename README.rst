django-template-helpers
=======================

.. image:: https://img.shields.io/pypi/v/django-template-helpers.svg
   :target: https://pypi.org/project/django-template-helpers/
   :alt: Latest Version

.. image:: https://github.com/stephrdev/django-template-helpers/workflows/Test/badge.svg?branch=master
   :target: https://github.com/stephrdev/django-template-helpers/actions?workflow=Test
   :alt: CI Status

.. image:: https://codecov.io/gh/stephrdev/django-template-helpers/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/stephrdev/django-template-helpers
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-template-helpers/badge/?version=latest
   :target: https://django-template-helpers.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status


*django-template-helpers* provides template tags to add missing features to the
Django template language.


Features
--------

* Template tag to set a new context variable ``set``
* Template filter to split a string into a list ``split``
* Context processor to expose selected settings to the templates
* GenericTemplateView for static pages


Requirements
------------

django-template-helpers supports Python 3 only and requires at least Django 1.11.


Prepare for development
-----------------------

A Python 3 interpreter is required in addition to poetry.

.. code-block:: shell

    $ poetry install


Now you're ready to run the tests:

.. code-block:: shell

    $ make tests
