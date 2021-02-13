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



.. code-block:: python

    from restpite import HttpGet
    from restpite import Model
    from listeners import MyListener

    class Car(Model):
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
