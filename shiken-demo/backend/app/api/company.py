from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select
from starlette.responses import Response

from app.deps.db import CurrentAsyncSession
from app.deps.request_params import CompRequestParams
from app.deps.users import CurrentUser
from app.models.comp import Comp
from app.schemas.comp import Comp as CompSchema
from app.schemas.comp import CompCreate, CompUpdate

router = APIRouter(prefix="/company")


@router.get("", response_model=List[CompSchema])
async def get_company(
    response: Response,
    session: CurrentAsyncSession,
    request_params: CompRequestParams,
    user: CurrentUser,
) -> Any:
    total = await session.scalar(
        select(func.count(Comp.id).filter(Comp.user_id == user.id))
    )
    company = (
        (
            await session.execute(
                select(Comp)
                .offset(request_params.skip)
                .limit(request_params.limit)
                .order_by(request_params.order_by)
                .filter(Comp.user_id == user.id)
            )
        )
        .scalars()
        .all()
    )
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(company)}/{total}"
    return company

@router.post("", response_model=CompSchema, status_code=201)
async def create_comp(
    comp_in: CompCreate,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    comp = Comp(**comp_in.dict())
    comp.user_id = user.id
    session.add(comp)
    await session.commit()
    return comp


@router.put("/{comp_id}", response_model=CompSchema)
async def update_comp(
    comp_id: int,
    comp_in: CompUpdate,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    comp: Optional[Comp] = await session.get(Comp, comp_id)
    if not comp or comp.user_id != user.id:
        raise HTTPException(404)
    update_data = comp_in.dict(exclude_unset=True)
    for field, value in update_data.company():
        setattr(comp, field, value)
    session.add(comp)
    await session.commit()
    return comp


@router.get("/{comp_id}", response_model=CompSchema)
async def get_comp(
    comp_id: int,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    comp: Optional[Comp] = await session.get(Comp, comp_id)
    if not comp or comp.user_id != user.id:
        raise HTTPException(404)
    return comp


@router.delete("/{comp_id}")
async def delete_comp(
    comp_id: int,
    session: CurrentAsyncSession,
    user: CurrentUser,
) -> Any:
    comp: Optional[Comp] = await session.get(Comp, comp_id)
    if not comp or comp.user_id != user.id:
        raise HTTPException(404)
    await session.delete(comp)
    await session.commit()
    return {"success": True}
