========
restpite
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

    from restpite import Request
    from models import Car

    def test_get_car(constants_provider) -> None:
        assert_that(
            Request(
                url="http://www.traffic.com/cars",
                query_params={'make': 'Audi', 'model': 'A4'},
                raise_on_failure=True,
                retryable=(5, RequestException),
                connect_timeout=30,
                read_timeout=15,
                hooks=[lambda x: print(x.json())]
            )
            .get()
            .status_code_is(200)
            .deserialize(Car).make).is_equal_to(constants_provider.AUDI)

----
