from typing import Dict

from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import json, text
from enum import Enum

from hermes.exceptions import BadRequest

from hermes.manager import AdminManager, AdminBatchManager


class AdminView(HTTPMethodView):
    AdminType = Enum("AdminType", ["ROOT", "ADMIN", "INTERVIEW"])
    manager = AdminManager()

    async def post(self, request: Request):
        admin_info: Dict = request.json

        try:
            admin_id = admin_info["id"]
            admin_name = admin_info["name"]
            admin_password = admin_info["password"]
            admin_type = self.AdminType(int(admin_info["type"]))
            admin_email = admin_info["email"]
        except KeyError as e:
            raise BadRequest(f"Invalid Parameter")

        await self.manager.register_admin(admin_id, admin_name, admin_email, admin_password, admin_type)

        return text("Successfully registered", status=200)


class AdminBatchView(HTTPMethodView):
    manager = AdminBatchManager()

    async def get(self, request: Request):
        search_option = request.args

        result = await self.manager.search_admins(**search_option)

        return json(result, status=200)


class AdminInfoView(HTTPMethodView):
    async def get(self, request, admin_id):
        return json(body={}, status=200)

    async def patch(self, request, admin_id):
        return json(body={}, status=200)

    async def delete(self, request, admin_id):
        return json(body={}, status=200)


class AuthenticationManager(HTTPMethodView):
    async def get(self, request):
        return json(body={}, status=200)


class UserView(HTTPMethodView):
    async def post(self, request):
        return json(body={}, status=200)


class UserBatchView(HTTPMethodView):
    async def get(self, request):
        return json(body={}, status=200)


class UserInfoView(HTTPMethodView):
    async def get(self, request, user_email):
        return json(body={}, status=200)

    async def patch(self, request, user_email):
        return json(body={}, status=200)

    async def delete(self, request, user_email):
        return json(body={}, status=200)


class UserStatusView(HTTPMethodView):
    async def get(self, request):
        return json(body={}, status=200)

    async def patch(self, request):
        return json(body={}, status=200)
