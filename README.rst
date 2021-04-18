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

Restpite is a simple python based HTTP DSL for testing restful web services easily.  It comes bundled with
some nice continuity features making it also a perfect for standalone scripts and non test related libraries,
however the focus here is on testing.  Restpite supports both HTTP/1 and HTTP/2 (where the server also supports it)
and offers both a syncronous (default) and Asyncronous client(s) where necessary.  Restpite is underpinned by
the wonderful `httpx` library (rather than `requests`).

Some of the features of Restpite are:

Aim of the library:

 - Easily write API wrappers for testing restful web services
 - Easily build HTTP based python scripts that require resiliency out of the box
 - Support fire & forget / libraries that deal primarily with HTTP but do not care about explicitly testing something
 - Support HTTP/1 and HTTP/2
 - Provide the capabilities for both `Sync` and `Async` capabilities

Outline of planned features:

 - Support for customisable, retryable requests (idempotent or not)
 - Support for all HTTP Verbs and permit user defined custom ones, `MKCOL` as an example
 - Inbuilt tracking of all HTTP traffic, permitting logging output
 - Pytest plugin `pytest-restpite` (way later on)
 - Powerful, Customisable `RestpiteResponse` deserialization to user defined objects
 - Ability to track performance metrics of all HTTP traffic
 - In built assertions to `RestpiteRequest` objects to make test writing clean and concise
 - Observable / Adapter system to allow client code to easily hook into the HTTP flow and modify behaviour
 - Resiliency notifications (minor use case but perhaps useful for some users)
 - Request-to-curl command output (easy recreation in test environments etc)
 - Allure integrations for continuous integration testing visibility / ease of use
 - English, readable DSL
 - Support for BDD scenario test writing (Given, Then, When etc)

----

A Trivial Example

.. code-block:: python

    from dataclasses import dataclass
    from restpite import get


    @dataclass
    class User:
        id: int
        name: str
        username: str
        phone: str
        website: str


    def test_my_api() -> None:
        url, expected = "https://jsonplaceholder.typicode.com/user/foo@bar.com", 11
        user = get(url).assert_was_ok().assert_application_json().deserialize(User)
        assert user.id == expected


Contributing
----

 .. code-block:: console

    git@github.com:symonk/restpite.git
    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[testing]"
    pre-commit install
    tox -e linting, py38
    push changes to upstream branch and open a pull request!
