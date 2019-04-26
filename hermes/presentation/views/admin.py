from typing import Union, List, Dict

from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import json

from hermes.repositories.connections import MySQLConnection, RedisConnection
from hermes.repositories.external_service import ExternalService, GatewayConnection

from hermes.adapters.repositories.admin import AdminRepositoryAdapter
from hermes.adapters.services.admin import AdminServiceAdapter


def _security_filter(admin_data: Union[List, Dict]):
    if isinstance(admin_data, list):
        for i in admin_data:
            del i["admin_password"]
    elif isinstance(admin_data, dict):
        del admin_data["admin_password"]


class AdminView(HTTPMethodView):
    repository = AdminRepositoryAdapter(MySQLConnection, RedisConnection)
    external_service = ExternalService(GatewayConnection)

    service = AdminServiceAdapter(repository, external_service)

    async def post(self, request: Request):
        admin_data = request.json

        await self.service.create(admin_data)

        return json({
            "msg": "successfully created"
        }, 201)


class AdminBatchView(HTTPMethodView):
    repository = AdminRepositoryAdapter(MySQLConnection, RedisConnection)
    external_service = ExternalService(GatewayConnection)

    service = AdminServiceAdapter(repository, external_service)

    async def get(self, request: Request):
        filters = request.args

        result = await self.service.get_list(filters)
        _security_filter(result)

        return json(result, 200)


class AdminDetailView(HTTPMethodView):
    repository = AdminRepositoryAdapter(MySQLConnection, RedisConnection)
    external_service = ExternalService(GatewayConnection)

    service = AdminServiceAdapter(repository, external_service)

    async def get(self, request: Request, admin_id: str):
        admin = await self.service.get_one(admin_id)
        _security_filter(admin)

        return json(admin, 200)

    async def patch(self, request: Request, admin_id: str):
        patch_data = request.json

        await self.service.patch(admin_id, patch_data)

        return json({
            "msg": "Successfully patched"
        }, 200)

    async def delete(self, request: Request, admin_id: str):
        await self.service.delete(admin_id)

        return json({
            "msg": "Successfully deleted"
        }, 200)
