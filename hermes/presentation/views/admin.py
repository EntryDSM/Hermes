from typing import Dict, List, Union

from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from werkzeug.security import check_password_hash

from hermes.adapters.repositories.admin import AdminRepositoryAdapter
from hermes.adapters.services.admin import AdminServiceAdapter
from hermes.misc.exceptions import BadRequest, Forbidden
from hermes.repositories.connections import MySQLConnection, RedisConnection
from hermes.repositories.external_service import GatewayConnection


def _security_filter(admin_data: Union[List, Dict]):
    if isinstance(admin_data, list):
        for i in admin_data:
            del i["admin_password"]
    elif isinstance(admin_data, dict):
        del admin_data["admin_password"]


class AdminView(HTTPMethodView):
    repository = AdminRepositoryAdapter(
        MySQLConnection, RedisConnection, GatewayConnection
    )
    service = AdminServiceAdapter(repository)

    async def post(self, request: Request):
        admin_data = request.json

        await self.service.create(admin_data)

        return json({"msg": "successfully created"}, 201)


class AdminBatchView(HTTPMethodView):
    repository = AdminRepositoryAdapter(
        MySQLConnection, RedisConnection, GatewayConnection
    )
    service = AdminServiceAdapter(repository)

    async def get(self, request: Request):
        filters = request.args

        result = await self.service.get_list(filters)
        _security_filter(result)

        return json(result, 200)


class AdminDetailView(HTTPMethodView):
    repository = AdminRepositoryAdapter(
        MySQLConnection, RedisConnection, GatewayConnection
    )
    service = AdminServiceAdapter(repository)

    async def get(self, request: Request, admin_id: str):
        admin = await self.service.get_one(admin_id)
        _security_filter(admin)

        return json(admin, 200)

    async def patch(self, request: Request, admin_id: str):
        patch_data = request.json

        await self.service.patch(admin_id, patch_data)

        return json({"msg": "Successfully patched"}, 200)

    async def delete(self, request: Request, admin_id: str):
        await self.service.delete(admin_id)

        return json({"msg": "Successfully deleted"}, 200)


class AdminAuthorizationView(HTTPMethodView):
    repository = AdminRepositoryAdapter(MySQLConnection, RedisConnection, GatewayConnection)
    service = AdminServiceAdapter(repository)

    async def post(self, request: Request, admin_id: str):
        password = request.json.get("password")
        if not password:
            raise BadRequest("Bad Request")

        admin = await self.service.get_one(admin_id)
        if not check_password_hash(admin["admin_password"], password):
            raise Forbidden("Authorization failed")

        return json({"msg": "Authorization succeed"}, 200)
