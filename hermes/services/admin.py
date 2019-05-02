from typing import Dict, List, Optional

from hermes.adapters.repositories.admin import AdminRepositoryAdapter
from hermes.entities.admin import Admin


class AdminService:
    def __init__(self, repository: AdminRepositoryAdapter):
        self.repository: AdminRepositoryAdapter = repository

    async def create(self, admin: Admin) -> None:
        await self.repository.save(admin)

    async def delete(self, admin_id: str) -> None:
        await self.repository.delete(admin_id)

    async def patch(self, admin_id: str, patch_data: Admin) -> None:
        await self.repository.patch(admin_id, patch_data)

    async def get_list(
        self, filters: Optional[Dict[str, str]] = None
    ) -> List[Optional[Admin]]:
        admins = await self.repository.get_list(filters)
        return admins

    async def get_one(self, admin_id: str) -> Optional[Admin]:
        admin = await self.repository.get_one(admin_id)
        return admin
