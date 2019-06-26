from typing import Any, Dict

from marshmallow import ValidationError
from sanic.exceptions import NotFound

from hermes.adapters import AbstractAdapter
from hermes.adapters.repositories.applicant_status import (
    ApplicantStatusRepositoryAdapter,
)
from hermes.adapters.schema import ApplicantStatusSchema, Schema
from hermes.entities.applicant_status import ApplicantStatus
from hermes.misc.exceptions import ApplicantNotFoundException, BadRequest
from hermes.services.applicant_status import ApplicantStatusService


class ApplicantStatusServiceAdapter(AbstractAdapter):
    schema = ApplicantStatusSchema()

    def __init__(self, repository: ApplicantStatusRepositoryAdapter):
        self.service = ApplicantStatusService(repository)

    async def init(self, email: str) -> Dict[str, Any]:
        await self.service.init(email)
        status = await self.service.get_one(email)
        return self._entity_to_data(self.schema, status)

    async def patch(self, email: str, patch_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            patch_data = self._data_to_entity(self.schema, patch_data)
        except ValidationError:
            raise BadRequest("Bad Request")

        try:
            await self.service.patch(email, patch_data)
        except ApplicantNotFoundException as e:
            raise NotFound(e.args[0])

        status = await self.service.get_one(email)
        return self._entity_to_data(self.schema, status)

    async def get_one(self, email: str) -> Dict[str, Any]:
        try:
            status = await self.service.get_one(email)
        except ApplicantNotFoundException as e:
            raise NotFound(e.args[0])

        return self._entity_to_data(self.schema, status)

    def _data_to_entity(self, schema: Schema, data: Dict[str, Any]) -> ApplicantStatus:
        return schema.load(data)

    def _entity_to_data(
        self, schema: Schema, entity: ApplicantStatus
    ) -> Dict[str, Any]:
        return schema.dump(entity)
