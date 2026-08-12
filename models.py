from pydantic import BaseModel

class Player(BaseModel):
    id: int
    name: str
    color: str
    batting: int
    pitching: int
    fielding: int
    running: int