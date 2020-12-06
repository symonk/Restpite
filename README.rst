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

    from restpite import given
    from mymodels import ModelClazz

    def test_the_post(user_fixture) -> None:
        given("https://www.myapi.com")
            .when()
            .post()
            .with_query_params({'user_id': user_fixture.id})
            .with_headers({'Content-type': 'content_type_value'})
            .then()
            .assert_that()
            .status_code(200)
            .deserialized(ModelClazz).some_field == 15
