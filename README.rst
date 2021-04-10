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

1. Automatic deserialization to python objects using marshmallow schemas
2. Robust RestpiteResponse objects with inbuilt assertions and assertion chaining
3. Listener system to allow client code to inspect traffic data easily
4. Powerful hooking system to allow client code to modify the behaviour of Restpite at runtime
5.  Fluent, English readable DSL
6.  Familiarity with the requests API for simple comfortability

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
    pip install -e ".[test]"
    pre-commit install
    tox -e linting, py38
