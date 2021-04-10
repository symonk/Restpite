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
