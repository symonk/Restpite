import random
from string import ascii_uppercase
from typing import Dict


def lower_case_headers_of_len(length: int = 2) -> Dict[str, str]:
    """
    Sample the lowercase ascii letters to return a dictionary of matching
    key: value pairs where both the key and value are the same letter randomly
    chosen.  This cannot produce duplicate(s)

    :param length: The total amount of non duplicate random keys to generate.
    """
    return {k: k for k in (random.sample(ascii_uppercase, length))}
