django-template-helpers
=======================

.. image:: https://img.shields.io/pypi/v/django-template-helpers.svg
   :target: https://pypi.org/project/django-template-helpers/
   :alt: Latest Version

.. image:: https://codecov.io/gh/moccu/django-template-helpers/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/moccu/django-template-helpers
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-template-helpers/badge/?version=latest
   :target: https://django-template-helpers.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/moccu/django-template-helpers.svg?branch=master
   :target: https://travis-ci.org/moccu/django-template-helpers


*django-template-helpers* provides template tags to add missing features to the
Django template language.


Features
--------

* Template tag to set a new context variable ``set``
* Template filter to split a string into a list ``split``
* Context processor to expose selected settings to the templates


Requirements
------------

django-template-helpers supports Python 3 only and requires at least Django 1.11.


Prepare for development
-----------------------

A Python 3.6 interpreter is required in addition to pipenv.

.. code-block:: shell

    $ pipenv install --python 3.6 --dev
    $ pipenv shell
    $ pip install -e .


Now you're ready to run the tests:

.. code-block:: shell

    $ pipenv run py.test


Resources
---------

* `Documentation <https://django-template-helpers.readthedocs.org/>`_
* `Bug Tracker <https://github.com/moccu/django-template-helpers/issues>`_
* `Code <https://github.com/moccu/django-template-helpers/>`_
