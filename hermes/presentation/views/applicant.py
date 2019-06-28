from typing import Dict, List, Union

from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from werkzeug.security import check_password_hash

from hermes.adapters.repositories.applicant import ApplicantRepositoryAdapter
from hermes.adapters.repositories.applicant_status import (
    ApplicantStatusRepositoryAdapter,
)
from hermes.adapters.services.applicant import ApplicantServiceAdapter
from hermes.adapters.services.applicant_status import ApplicantStatusServiceAdapter
from hermes.misc.exceptions import BadRequest, Forbidden
from hermes.repositories.connections import MySQLConnection, RedisConnection


def _security_filter(unfiltered_data: Union[List, Dict]):
    if isinstance(unfiltered_data, list):
        for unfiltered_data_object in unfiltered_data:
            del unfiltered_data_object["password"]
    elif isinstance(unfiltered_data, dict):
        del unfiltered_data["password"]


class ApplicantView(HTTPMethodView):
    applicant_repository = ApplicantRepositoryAdapter(MySQLConnection, RedisConnection)
    status_repository = ApplicantStatusRepositoryAdapter(
        MySQLConnection, RedisConnection
    )

    applicant_service = ApplicantServiceAdapter(applicant_repository)
    status_service = ApplicantStatusServiceAdapter(status_repository)

    async def post(self, request: Request):
        applicant = request.json
        applicant = await self.applicant_service.create(applicant)
        status = await self.status_service.init(applicant["email"])

        _security_filter(applicant)
        del status["applicant_email"]
        applicant.update({"status": status})

        return json(applicant, 201)


class ApplicantBatchView(HTTPMethodView):
    repository = ApplicantRepositoryAdapter(MySQLConnection, RedisConnection)
    service = ApplicantServiceAdapter(repository)

    async def get(self, request: Request):
        filters = request.args

        applicants = await self.service.get_list(filters)
        _security_filter(applicants)

        return json(applicants, 200)


class ApplicantDetailView(HTTPMethodView):
    repository = ApplicantRepositoryAdapter(MySQLConnection, RedisConnection)
    service = ApplicantServiceAdapter(repository)

    async def get(self, request: Request, email: str):
        applicant = await self.service.get_one(email)
        _security_filter(applicant)

        return json(applicant, 200)

    async def patch(self, request: Request, email: str):
        patch_data = request.json
        applicant = await self.service.patch(email, patch_data)
        _security_filter(applicant)

        return json(applicant, 200)

    async def delete(self, request: Request, email: str):
        await self.service.delete(email)

        return json({"msg": "Successfully deleted"}, 200)


class ApplicantAuthorizationView(HTTPMethodView):
    repository = ApplicantRepositoryAdapter(MySQLConnection, RedisConnection)
    service = ApplicantServiceAdapter(repository)

    async def post(self, request: Request, email: str):
        password = request.json.get("password")
        if not password:
            raise BadRequest("Bad Request")

        applicant = await self.service.get_one(email)
        if not check_password_hash(applicant["password"], password):
            raise Forbidden("Authorization failed")

        return json({"msg": "Authorization succeed"}, 200)
