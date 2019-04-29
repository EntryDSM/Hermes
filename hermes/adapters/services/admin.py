from typing import Any, Dict, List, Optional

from marshmallow import ValidationError
from pymysql.err import InternalError
from sanic.exceptions import NotFound

from hermes.adapters import AbstractAdapter
from hermes.adapters.repositories.admin import AdminRepositoryAdapter
from hermes.adapters.schema import AdminPatchSchema, AdminSchema, Schema
from hermes.entities.admin import Admin
from hermes.misc.exceptions import (AdminAlreadyExistException,
                                    AdminNotFoundException, BadRequest,
                                    Conflict)
from hermes.repositories.external_service import ExternalService
from hermes.services.admin import AdminService


class AdminServiceAdapter(AbstractAdapter):
    schema = AdminSchema()
    patch_schema = AdminPatchSchema()

    def __init__(
        self, repository: AdminRepositoryAdapter, external_service: ExternalService
    ):
        self.service = AdminService(repository, external_service)

    async def create(self, admin_data: Dict[str, str]) -> None:
        try:
            admin = self._data_to_entity(self.schema, admin_data)
        except ValidationError:
            raise BadRequest("Request again with acceptable payload")

        try:
            await self.service.create(admin)
        except AdminAlreadyExistException as e:
            raise Conflict(e.args[0])

    async def delete(self, admin_id: str) -> None:
        try:
            await self.service.delete(admin_id)
        except AdminNotFoundException as e:
            raise NotFound(e.args[0])

    async def patch(self, admin_id: str, patch_data: Dict[str, str]) -> None:
        try:
            patch_data = self._data_to_entity(self.patch_schema, patch_data)
        except ValidationError:
            raise BadRequest("Request again with acceptable payload")

        try:
            await self.service.patch(admin_id, patch_data)
        except AdminNotFoundException as e:
            raise NotFound(e.args[0])

    async def get_list(
        self, filters: Optional[Dict[str, str]]
    ) -> List[Optional[Dict[str, str]]]:
        try:
            admin_list = await self.service.get_list(filters)
        except InternalError:
            raise BadRequest("Unknown query argument")

        return [self._entity_to_data(self.schema, data) for data in admin_list]

    async def get_one(self, admin_id: str):
        try:
            admin = await self.service.get_one(admin_id)
        except AdminNotFoundException as e:
            raise NotFound(e.args[0])

        return self._entity_to_data(self.schema, admin)

    def _data_to_entity(self, schema: Schema, data: Dict[str, Any]) -> Dict[str, Any]:
        return schema.load(data)

    def _entity_to_data(self, schema: Schema, entity: Admin) -> Dict[str, Any]:
        return schema.dump(entity)
