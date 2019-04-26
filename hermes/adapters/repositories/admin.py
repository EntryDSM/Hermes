from dataclasses import asdict
from typing import Type, Optional, Dict, List, Any

from marshmallow import Schema
from pymysql.err import IntegrityError

from hermes.adapters import AbstractAdapter
from hermes.entities.admin import Admin
from hermes.repositories.admin import AdminPersistentRepository, AdminCacheRepository
from hermes.repositories.connections import DBConnection, CacheConnection
from hermes.misc.exceptions import AdminAlreadyExistException, AdminNotFoundException


class AdminRepositoryAdapter(AbstractAdapter):
    def __init__(self, db_connection: Type[DBConnection], cache_connection: Type[CacheConnection]):
        self.persistence_repository = AdminPersistentRepository(db_connection)
        self.cache_repository = AdminCacheRepository(cache_connection)

    async def save(self, admin: Dict[str, Any]):
        try:
            await self.persistence_repository.save(admin)
        except IntegrityError:
            raise AdminAlreadyExistException("Admin Already Exists")
        await self.cache_repository.set(admin)

    async def delete(self, admin_id: str):
        await self.persistence_repository.delete(admin_id)
        await self.cache_repository.delete(admin_id)

    async def patch(self, admin_id: str, patch_data: Dict[str, str]):
        await self.persistence_repository.patch(admin_id, patch_data)
        await self.cache_repository.delete(admin_id)

    async def get_list(self, filters: Optional[Dict[str, str]] = None) -> List[Optional[Admin]]:
        data_list = await self.persistence_repository.get_list(filters)
        return [self._data_to_entity(data) for data in data_list]

    async def get_one(self, admin_id: str) -> Optional[Admin]:
        data = await self.cache_repository.get(admin_id)
        if not data:
            data = await self.persistence_repository.get_one(admin_id)
            if not data:
                raise AdminNotFoundException("Not Found")

        await self.cache_repository.set(data)
        return self._data_to_entity(data)

    @classmethod
    def _entity_to_data(cls, schema: Schema, entity: Admin) -> Dict[str, Any]:
        return asdict(entity)

    @classmethod
    def _data_to_entity(cls, schema: Schema, data: Dict[str, Any]) -> Admin:
        return Admin(**data)
