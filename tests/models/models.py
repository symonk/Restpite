from marshmallow_dataclass import dataclass


@dataclass
class Car:
    colour: str
    brand: str
    engine: int
