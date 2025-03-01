from typing import Any, List, Optional

from app.deps.db import CurrentAsyncSession
from app.deps.request_params import CompanyRequestParams
from app.deps.users import CurrentUser
from app.models.company import Company
from app.schemas.company import Company as CompanySchema
from app.schemas.company import CompanyCreate, CompanyUpdate
from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from starlette.responses import Response

router = APIRouter(prefix="/companys")


@router.get("", response_model=List[CompanySchema])
async def get_companys(
    response: Response,
    session: CurrentAsyncSession,
    request_params: CompanyRequestParams,
) -> Any:
    total = await session.scalar(
        select(func.count(Company.id))
    )
    companys = (
        (
            await session.execute(
                select(Company)
                .offset(request_params.skip)
                .limit(request_params.limit)
                .order_by(request_params.order_by)
            )
        )
        .scalars()
        .all()
    )
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(companys)}/{total}"
    return companys


@router.post("", response_model=CompanySchema, status_code=201)
async def create_company(
    company_in: CompanyCreate,
    session: CurrentAsyncSession,
) -> Any:
    company = Company(**company_in.dict())
    session.add(company)
    await session.commit()
    return company


@router.put("/{company_id}", response_model=CompanySchema)
async def update_company(
    company_id: int,
    company_in: CompanyUpdate,
    session: CurrentAsyncSession,
) -> Any:
    company: Optional[Company] = await session.get(Company, company_id)
    if not company:
        raise HTTPException(404)
    update_data = company_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    session.add(company)
    await session.commit()
    return company


@router.get("/{company_id}", response_model=CompanySchema)
async def get_company(
    company_id: int,
    session: CurrentAsyncSession,
) -> Any:
    company: Optional[Company] = await session.get(Company, company_id)
    if not company:
        raise HTTPException(404)
    return company


@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    session: CurrentAsyncSession,
) -> Any:
    company: Optional[Company] = await session.get(Company, company_id)
    if not company:
        raise HTTPException(404)
    await session.delete(company)
    await session.commit()
    return {"success": True}
