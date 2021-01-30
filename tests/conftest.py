import random
from string import ascii_lowercase

import pytest


@pytest.fixture
def randomised_dict():
    return {random.choice(ascii_lowercase): random.choice(range(100)) for _ in range(5)}
