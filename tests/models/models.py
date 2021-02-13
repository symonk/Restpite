from pydantic import BaseModel


class Car(BaseModel):
    colour: str
    brand: str
    engine: int
