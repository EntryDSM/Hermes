from typing import Any, Dict, List, Optional, Type

from pymysql.err import IntegrityError

from hermes.adapters import AbstractAdapter
from hermes.adapters.schema import AdminSchema, Schema
from hermes.entities.admin import Admin
from hermes.misc.exceptions import AdminAlreadyExistException, AdminNotFoundException
from hermes.repositories.admin import AdminCacheRepository, AdminPersistentRepository
from hermes.repositories.connections import CacheConnection, DBConnection
from hermes.repositories.external_service import ExternalService, GatewayConnection


class AdminRepositoryAdapter(AbstractAdapter):
    schema = AdminSchema()

    def __init__(
        self,
        db_connection: Type[DBConnection],
        cache_connection: Type[CacheConnection],
        gateway_connection: Type[GatewayConnection],
    ):
        self.persistence_repository = AdminPersistentRepository(db_connection)
        self.cache_repository = AdminCacheRepository(cache_connection)
        self.external_service = ExternalService(gateway_connection)

    async def save(self, admin: Admin):
        admin = self._entity_to_data(self.schema, admin)

        try:
            await self.persistence_repository.save(admin)
        except IntegrityError:
            raise AdminAlreadyExistException("Admin Already Exists")

        await self.cache_repository.set(admin)
        await self.external_service.register_admin_to_gateway(admin["admin_id"])

    async def delete(self, admin_id: str):
        await self.persistence_repository.delete(admin_id)
        await self.cache_repository.delete(admin_id)
        await self.external_service.delete_tokens_from_gateway(admin_id)

    async def patch(self, admin_id: str, patch_data: Admin):
        patch_data = self._entity_to_data(self.schema, patch_data)

        if not await self.persistence_repository.get_one(admin_id):
            raise AdminNotFoundException("Not Found")

        await self.persistence_repository.patch(admin_id, patch_data)
        await self.cache_repository.delete(admin_id)
        await self.external_service.delete_tokens_from_gateway(admin_id)

    async def get_list(
        self, filters: Optional[Dict[str, str]] = None
    ) -> List[Optional[Admin]]:
        data_list = await self.persistence_repository.get_list(filters)
        return [self._data_to_entity(self.schema, data) for data in data_list]

    async def get_one(self, admin_id: str) -> Optional[Admin]:
        data = await self.cache_repository.get(admin_id)
        if not data:
            data = await self.persistence_repository.get_one(admin_id)
            if not data:
                raise AdminNotFoundException("Not Found")

        await self.cache_repository.set(data)
        return self._data_to_entity(self.schema, data)

    def _data_to_entity(self, schema: Schema, data: Dict[str, Any]) -> Admin:
        return schema.load(data)

    def _entity_to_data(self, schema: Schema, entity: Admin) -> Dict[str, Any]:
        return schema.dump(entity)
