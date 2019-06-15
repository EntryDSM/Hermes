from typing import Any, Dict, List, Optional

from sanic.exceptions import NotFound

from hermes.adapters import AbstractAdapter
from hermes.adapters.repositories.applicant import (
    ApplicantRepositoryAdapter,
)
from hermes.adapters.schema import (
    ApplicantPatchSchema,
    ApplicantSchema,
    Schema,
)
from hermes.entities.applicant import Applicant
from hermes.misc.exceptions import (
    ApplicantAlreadyExistException,
    ApplicantNotFoundException,
    Conflict,
)
from hermes.services.applicant import ApplicantService


class ApplicantServiceAdapter(AbstractAdapter):
    schema = ApplicantSchema()
    patch_schema = ApplicantPatchSchema()

    def __init__(self, repository: ApplicantRepositoryAdapter):
        self.service = ApplicantService(repository)

    async def create(self, init_applicant_data: Dict[str, Any]) -> Dict[str, Any]:
        entity = self._data_to_entity(self.schema, init_applicant_data)

        try:
            await self.service.create(entity)
        except ApplicantAlreadyExistException as e:
            raise Conflict(e.args[0])

        applicant = await self.service.get_one(entity.email)
        return self._entity_to_data(self.schema, applicant)

    async def patch(self, email: str, patch_data: Dict[str, Any]) -> Dict[str, Any]:
        entity = self._data_to_entity(self.patch_schema, patch_data)

        try:
            await self.service.patch(email, entity)
        except ApplicantNotFoundException as e:
            raise NotFound(e.args[0])

        applicant = await self.service.get_one(email)
        return self._entity_to_data(self.schema, applicant)

    async def delete(self, email: str) -> None:
        try:
            await self.service.delete(email)
        except ApplicantNotFoundException as e:
            raise NotFound(e.args[0])

    async def get_one(self, email: str) -> Dict[str, Any]:
        try:
            applicant: Applicant = await self.service.get_one(email)
        except ApplicantNotFoundException as e:
            raise NotFound(e.args[0])

        return self._entity_to_data(self.schema, applicant)

    async def get_list(
        self, filters: Optional[Dict[str, str]] = None
    ) -> List[Optional[Dict[str, str]]]:
        applicants = await self.service.get_list(filters)

        return [self._entity_to_data(self.schema, data) for data in applicants]

    def _data_to_entity(self, schema: Schema, data: Dict[str, Any]) -> Applicant:
        return schema.load(data)

    def _entity_to_data(self, schema: Schema, entity: Applicant) -> Dict[str, Any]:
        return schema.dump(entity)


