========
Restpite
========


.. image:: https://img.shields.io/pypi/v/restpite.svg
        :target: https://pypi.python.org/pypi/restpite

.. image:: https://travis-ci.com/symonk/Restpite.svg?branch=master
        :target: https://travis-ci.com/symonk/restpite

.. image:: https://readthedocs.org/projects/restpite/badge/?version=latest
        :target: https://restpite.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/symonk/Restpite/shield.svg
     :target: https://pyup.io/account/repos/github/symonk/Restpite/
     :alt: Updates

.. code-block:: python

    from restpite import Request
    from mymodels import ModelClazz

    def test_the_post(user_fixture) -> None:
        assert_that(
            Request(url="http://www.google.com")
            .raise_on_failure()
            .retry(5)
            .with_query_params(example_params)
            .send()
            .status_code
        ).is_equal_to(200)
