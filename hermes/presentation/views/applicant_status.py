from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from hermes.adapters.repositories.applicant_status import ApplicantStatusRepositoryAdapter
from hermes.adapters.services.applicant_status import ApplicantStatusServiceAdapter
from hermes.repositories.connections import MySQLConnection, RedisConnection


class ApplicantStatusView(HTTPMethodView):
    repository = ApplicantStatusRepositoryAdapter(
        MySQLConnection, RedisConnection
    )
    service = ApplicantStatusServiceAdapter(repository)

    async def patch(self, request: Request, email: str):
        patch_data = request.json
        status = await self.service.patch(email, patch_data)
        del status["applicant_email"]

        return json(status, 200)

    async def get(self, request: Request, email: str):
        status = await self.service.get_one(email)
        del status["applicant_email"]

        return json(status, 200)