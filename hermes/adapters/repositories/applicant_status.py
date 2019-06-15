from typing import Type, Dict, Any

from marshmallow import Schema

from hermes.adapters import AbstractAdapter
from hermes.adapters.schema import ApplicantStatusSchema
from hermes.entities.applicant_status import ApplicantStatus
from hermes.misc.exceptions import ApplicantNotFoundException, ApplicantStatusNotFoundException
from hermes.repositories.applicant_status import ApplicantStatusPersistentRepository, ApplicantStatusCacheRepository
from hermes.repositories.connections import DBConnection, CacheConnection


class ApplicantStatusRepositoryAdapter(AbstractAdapter):
    schema = ApplicantStatusSchema()

    def __init__(
        self,
        db_connection: Type[DBConnection],
        cache_connection: Type[CacheConnection],
    ):
        self.persistence_repository = ApplicantStatusPersistentRepository(db_connection)
        self.cache_repository = ApplicantStatusCacheRepository(cache_connection)

    async def init(self, email: str):
        await self.persistence_repository.init(email)

    async def patch(self, email: str, patch_data: ApplicantStatus) -> None:
        if not await self.persistence_repository.get_one(email):
            raise ApplicantNotFoundException("Not Found")

        patch_data = self._entity_to_data(self.schema, patch_data)

        await self.persistence_repository.patch(email, patch_data)
        await self.cache_repository.delete(email)

    async def get_one(self, email: str) -> ApplicantStatus:
        data = await self.cache_repository.get(email)

        if not data:
            data = await self.persistence_repository.get_one(email)
            if not data:
                raise ApplicantStatusNotFoundException("Not Found")

        await self.cache_repository.set(data)
        return self._data_to_entity(self.schema, data)

    def _data_to_entity(self, schema: Schema, data: Dict[str, Any]) -> ApplicantStatus:
        return schema.load(data)

    def _entity_to_data(self, schema: Schema, entity) -> Dict[str, Any]:
        return schema.dump(entity)