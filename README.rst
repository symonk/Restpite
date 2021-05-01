.. image:: .github/.images/logo.png
  :class: with-border
  :width: 1280

========
Restpite
========


.. image:: https://img.shields.io/pypi/v/restpite.svg
        :target: https://pypi.python.org/pypi/restpite

.. image:: https://github.com/symonk/restpite/actions/workflows/python-package.yml/badge.svg
        :target: https://github.com/symonk/restpite/actions

.. image:: https://readthedocs.org/projects/restpite/badge/?version=latest
        :target: https://restpite.readthedocs.io/en/latest/
        :alt: Documentation Status

.. image:: https://codecov.io/gh/symonk/restpite/branch/master/graph/badge.svg?token=E7SVA868NR
    :target: https://codecov.io/gh/symonk/restpite


----

Restpite is a simple python based HTTP DSL for testing restful web services easily.  Supporting both HTTP/1.1 and
HTTP/2 with both a `sync`` and `async` capable client.  Whether you are writing standalone scripts
or end to end system tests for a restful web service, restpite is the library for you.

Features of restpite:

 - Supports HTTP/1.1 & HTTP/2
 - Client supports both `sync` and `async` to avoid needlessly blocking on IO operations like requests
 - Extendable handler and hook dispatching system to allow client code to intercept HTTP flow
 - Powerful in built assertions for everything imaginable on your response objects
 - Integrates gracefully with marshmallow to easily deserialize response json into python objects
 - Intuitive DSL, underpinned by the brilliant `httpx` library
 - Automatic and customisable performance and request-response tracking in various formats
 - Tons of other cool features

----

<p align="center">&mdash; ⭐️ &mdash;</p>
