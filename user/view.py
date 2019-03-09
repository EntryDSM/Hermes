from sanic.views import HTTPMethodView
from sanic.response import json


class Status(HTTPMethodView):
    manager = StatusManager()

    async def get(self, request):
        return json(body={}, status=200)

    async def patch(self, request):
        return json(body={}, status=200)


class User(HTTPMethodView):
    manager = UserManager()

    async def get(self, request):
        return json(body={}, status=200)

    async def post(self, request):
        return json(body={}, status=200)

    async def patch(self, request):
        return json(body={}, status=200)



