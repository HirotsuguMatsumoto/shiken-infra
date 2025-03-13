from pydantic import BaseModel


class CompCreate(BaseModel):
    value: str


class CompUpdate(CompCreate):
    pass


class Comp(CompCreate):
    id: int

    class Config:
        orm_mode = True
