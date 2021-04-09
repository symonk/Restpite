.. image:: .github/.images/logo.png
  :class: with-border
  :width: 1280

========
Restpite
========


.. image:: https://img.shields.io/pypi/v/restpite.svg
        :target: https://pypi.python.org/pypi/restpite

.. image:: https://travis-ci.com/symonk/restpite.svg?branch=master
        :target: https://travis-ci.com/symonk/restpite

.. image:: https://readthedocs.org/projects/restpite/badge/?version=latest
        :target: https://restpite.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/symonk/restpite/shield.svg
     :target: https://pyup.io/account/repos/github/symonk/restpite/
     :alt: Updates


.. image:: https://codecov.io/gh/symonk/restpite/branch/master/graph/badge.svg?token=E7SVA868NR
    :target: https://codecov.io/gh/symonk/restpite

----

Restpite is a simple python based HTTP DSL for testing restful web services easily.  It comes bundled with
some nice continuity features making it also a perfect for standalone scripts and non test related libraries,
however the focus here is on testing.  Some of the features of Restpite are:

    - Automatic deserialization to python objects using marshmallow schemas
    - Robust RestpiteResponse objects with inbuilt assertions and assertion chaining
    - Listener system to allow client code to inspect traffic data easily
    - Powerful hooking system to allow client code to modify the behaviour of Restpite at runtime
    - Fluent, English readable DSL
    - Familiarity with the requests API for simple comfortability

----

Contributing
----

 - Clone the git repository
 - python -m venv .venv
 - source .venv/bin/activate (unix) .venv\Scripts\activate (windows)
 - pip install -e ".[test]"
 - pre-commit install
 - Make changes, stage & commit changes (this will auto run the linting stage and un-stage git hook failures)
 - tox -e linting | tox -e py38
