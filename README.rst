========
Restpite
========


.. image:: https://img.shields.io/pypi/v/restpite.svg
        :target: https://pypi.python.org/pypi/restpite

.. image:: https://img.shields.io/travis/symonk/restpite.svg
        :target: https://travis-ci.com/symonk/restpite

.. image:: https://readthedocs.org/projects/restpite/badge/?version=latest
        :target: https://restpite.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/symonk/restpite/shield.svg
     :target: https://pyup.io/repos/github/symonk/restpite/
     :alt: Updates



Python DSL for easily testing REST services.


* Free software: MIT license
* Documentation: https://restpite.readthedocs.io.


# Simple Use case:
----

.. code-block:: python

    from restpite import Given

    def test_the_post(user_fixture) -> None:
        Given("https://www.myapi.com")
            .When()
            .post()
            .with_query_params({'user_id': user_fixture.id})
            .with_headers({'Content-type': 'content_type_value'})
            .Then()
            .status_code().equals(200)
            .body('result').equals("updated resource")
