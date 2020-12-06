from restpite import given


def test_query_string_params() -> None:
    example_params = {"one": "one", "two": "two", "three": "three"}
    expected = "http://www.google.com?one=one&two=two&three=three"
    assert (
        given(raise_when_unsuccessful=True)
        .retry(1)
        .when("http://www.google.com")
        .with_query_params(example_params)
        .url
        == expected
    )
