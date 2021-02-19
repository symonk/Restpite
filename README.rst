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

Restpite is a simple python HTTP DSL for testing restful services, the easy way.  It sits on top of the
brilliant python `requests` library but provides some test friendly improvements.  Restpite aims to be
a great library for not only testing, but for standalone scripts and libraries that want functionality
such as continuity using things like Restpite's `Retry` capabilities out of the box without having to
roll their own adapters / interact with `urllib` directly.  Restpite offers:

  - Powerful deserialization to user defined models
  - Abundance of custom adapters for use in standalone scripts and libraries not test relatable
  - Built in assertion and chaining functionality to the `HttpResponse` objects
  - Powerful hooking system to implement custom behaviour around all HTTP traffic
  - Fluent, english readable DSL
  - Similarity to `requests` syntax to speed up the development process
  - (Coming later) BDD syntax support such as `Given()`, `When()` and `Then()`

----

A simple example:

.. code-block:: python

    from restpite import HttpGet
    from restpite import dataclass
    from listeners import MyListener

    @dataclass
    class Car:
        colour: str
        make: str
        model: str
        engine: float


    def test_get_car(constants_provider) -> None:
        assert_that(
            HttpGet(
                url="http://www.traffic.com/cars",
                query_params={'make': 'Audi', 'model': 'A4'},
                raise_on_failure=True,
                retryable=(5, RequestException),
                connect_timeout=30,
                read_timeout=15,
                listeners=MyListener()
            )
            .assert_was_ok()
            .deserialize(Car)).is_instance(Car)

----
