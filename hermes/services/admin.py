from typing import Any, Dict, List, Optional

from hermes.adapters.repositories.admin import AdminRepositoryAdapter
from hermes.entities.admin import Admin
from hermes.repositories.external_service import ExternalService


class AdminService:
    def __init__(
        self, repository: AdminRepositoryAdapter, external_service_api: ExternalService
    ):
        self.repository: AdminRepositoryAdapter = repository
        self.external_service: ExternalService = external_service_api

    async def create(self, admin: Dict[str, Any]) -> None:
        await self.repository.save(admin)
        await self.external_service.register_admin_to_gateway(admin["admin_id"])

    async def delete(self, admin_id: str) -> None:
        await self.repository.delete(admin_id)
        await self.external_service.delete_tokens_from_gateway(admin_id)

    async def patch(self, admin_id: str, patch_data: Dict[str, str]) -> None:
        await self.repository.patch(admin_id, patch_data)
        await self.external_service.delete_tokens_from_gateway(admin_id)

    async def get_list(self, filters: Dict[str, str]) -> List[Optional[Admin]]:
        admins = await self.repository.get_list(filters)
        return admins

    async def get_one(self, admin_id: str) -> Optional[Admin]:
        admin = await self.repository.get_one(admin_id)
        return admin
