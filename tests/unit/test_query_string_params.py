from restpite import Given


def test_query_string_params() -> None:
    example_params = {"one": "one", "two": "two", "three": "three"}
    expected = "http://www.google.com?one=one&two=two&three=three"
    assert Given(url="http://www.google.com", q_string=example_params).url == expected
