from typing import Dict

from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.response import json,text
from enum import Enum

from hermes.manager import AdminManager


class AdminView(HTTPMethodView):
    async def post(self, request):
        return json(body={}, status=200)


class AdminBatchView(HTTPMethodView):
    async def get(self, request):
        return json(body={}, status=200)


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
