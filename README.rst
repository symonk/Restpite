.. image:: .github/.images/logo.png
  :class: with-border
  :width: 1280

========
Restpite
========


.. image:: https://github.com/symonk/restpite/actions/workflows/python-package.yml/badge.svg
        :target: https://github.com/symonk/restpite/actions

.. image:: https://github.com/symonk/restpite/actions/workflows/python-package.yml/badge.svg
        :target: https://github.com/symonk/restpite/actions/workflows/python-package.yml/badge.svg

.. image:: https://readthedocs.org/projects/restpite/badge/?version=latest
        :target: https://restpite.readthedocs.io/en/latest/
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

Aim of the library:

 - Easily write API wrappers for testing restful web services
 - Easily build HTTP based python scripts that require resiliency out of the box
 - Support fire & forget / libraries that deal primarily with HTTP but do not care about explicitly testing something

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
    from dataclasses import field
    from typing import List

    from restpite import get


    @dataclass
    class Geo:
        lat: str
        long: str


    @dataclass
    class Address:
        street: str
        suite: str
        city: str
        zipcode: str
        geo: Geo


    @dataclass
    class Company:
        name: str
        catchPhrase: str
        bs: str


    @dataclass
    class User:
        id: int
        name: str
        username: str
        address: Address
        phone: str
        website: str
        company: Company


    @dataclass
    class Users:
        users: List[User] = field(default_factory=list)


    def test_my_api() -> None:
        url = "https://jsonplaceholder.typicode.com/users"
        users = get(url).assert_was_ok().assert_application_json().deserialize(Users)
        assert len(users) == 10


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
