from pydantic import BaseModel, ConfigDict


class CompanyCreate(BaseModel):
    name: str


class CompanyUpdate(CompanyCreate):
    pass


class Company(CompanyCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
