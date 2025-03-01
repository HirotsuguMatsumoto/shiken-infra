from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str


class CompanyUpdate(CompanyCreate):
    pass


class Company(CompanyCreate):
    id: int

    class Config:
        orm_mode = True
