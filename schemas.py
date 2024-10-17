from pydantic import BaseModel

class Character(BaseModel):
    id: int
    name: str
    race: str
    age: int
    height: float

    class Config:
        orm_mode = True
