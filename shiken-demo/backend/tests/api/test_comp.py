from httpx import AsyncClient

from app.core.config import settings
from app.models.comp import Comp
from app.models.user import User
from tests.utils import get_jwt_header

      
class TestGetComapany:
    async def test_get_company_not_logged_in(self, client: AsyncClient):
        resp = await client.get(settings.API_PATH + "/company")
        assert resp.status_code == 401

    async def test_get_company(self, client: AsyncClient, create_user, create_comp):
        user: User = await create_user()
        await create_comp(user=user)
        jwt_header = get_jwt_header(user)
        resp = await client.get(settings.API_PATH + "/company", headers=jwt_header)
        assert resp.status_code == 200
        assert resp.headers["Content-Range"] == "0-1/1"
        assert len(resp.json()) == 1



class TestGetSingleComp:
    async def test_get_single_comp(self, client: AsyncClient, create_user, create_comp):
        user: User = await create_user()
        comp: Comp = await create_comp(user=user)
        jwt_header = get_jwt_header(user)
        resp = await client.get(
            settings.API_PATH + f"/company/{comp.id}", headers=jwt_header
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["id"] == comp.id
        assert data["value"] == comp.value


class TestCreateComp:
    async def test_create_comp(self, client: AsyncClient, create_user):
        user: User = await create_user()
        jwt_header = get_jwt_header(user)

        resp = await client.post(
            settings.API_PATH + "/company", headers=jwt_header, json={"value": "value"}
        )
        assert resp.status_code == 201, resp.text
        assert resp.json()["id"]


class TestDeleteComp:
    async def test_delete_comp(self, client: AsyncClient, create_user, create_comp):
        user: User = await create_user()
        comp: Comp = await create_comp(user=user)
        jwt_header = get_jwt_header(user)

        resp = await client.delete(
            settings.API_PATH + f"/company/{comp.id}", headers=jwt_header
        )
        assert resp.status_code == 200

    async def test_delete_comp_does_not_exist(self, client: AsyncClient, create_user):
        user: User = await create_user()
        jwt_header = get_jwt_header(user)

        resp = await client.delete(
            settings.API_PATH + f"/company/{10**6}", headers=jwt_header
        )
        assert resp.status_code == 404, resp.text


class TestUpdateComp:
    async def test_update_comp(self, client: AsyncClient, create_user, create_comp):
        user: User = await create_user()
        comp: Comp = await create_comp(user=user)
        jwt_header = get_jwt_header(user)

        resp = await client.put(
            settings.API_PATH + f"/company/{comp.id}",
            headers=jwt_header,
            json={"value": "new value"},
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["value"] == "new value"
