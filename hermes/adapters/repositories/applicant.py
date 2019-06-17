from typing import Any, Dict, List, Optional, Type

from marshmallow import Schema
from pymysql import IntegrityError

from hermes.adapters import AbstractAdapter
from hermes.adapters.schema import (
    ApplicantPatchSchema,
    ApplicantSchema,
)
from hermes.entities.applicant import Applicant
from hermes.misc.exceptions import (
    ApplicantAlreadyExistException,
    ApplicantNotFoundException,
)
from hermes.repositories.applicant import (
    ApplicantCacheRepository,
    ApplicantPersistentRepository,
)
from hermes.repositories.connections import CacheConnection, DBConnection


class ApplicantRepositoryAdapter(AbstractAdapter):
    schema = ApplicantSchema()
    patch_schema = ApplicantPatchSchema()

    def __init__(
        self,
        db_connection: Type[DBConnection],
        cache_connection: Type[CacheConnection],
    ):

        self.persistence_repository = ApplicantPersistentRepository(db_connection)
        self.cache_repository = ApplicantCacheRepository(cache_connection)

    async def save(self, email: str, password: str) -> None:
        try:
            await self.persistence_repository.save(email, password)
        except IntegrityError:
            raise ApplicantAlreadyExistException("Applicant Already Exists")

    async def patch(self, email: str, patch_data: Applicant) -> None:
        if not await self.persistence_repository.get_one(email):
            raise ApplicantNotFoundException("Not Found")

        patch_data = self._entity_to_data(self.patch_schema, patch_data)

        await self.persistence_repository.patch(email, patch_data)
        await self.cache_repository.delete(email)

    async def delete(self, email: str) -> None:
        if not await self.persistence_repository.get_one(email):
            raise ApplicantNotFoundException("Not Found")

        await self.persistence_repository.delete(email)
        await self.cache_repository.delete(email)

    async def get_one(self, email: str) -> Applicant:
        data = await self.cache_repository.get(email)

        if not data:
            data = await self.persistence_repository.get_one(email)
            if not data:
                raise ApplicantNotFoundException("Not Found")

        await self.cache_repository.set(data)
        return self._data_to_entity(self.schema, data)

    async def get_list(
        self, filters: Optional[Dict[str, str]] = None
    ) -> List[Applicant]:
        data_list = await self.persistence_repository.get_list(filters)
        return [self._data_to_entity(self.schema, data) for data in data_list]

    def _data_to_entity(self, schema: Schema, data: Dict[str, Any]) -> Applicant:
        return schema.load(data)

    def _entity_to_data(self, schema: Schema, entity) -> Dict[str, Any]:
        return schema.dump(entity)


