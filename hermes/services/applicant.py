from typing import Any, Dict, List, Optional

from hermes.adapters.repositories.applicant import (
    ApplicantRepositoryAdapter,
)
from hermes.entities.applicant import Applicant


class ApplicantService:
    def __init__(self, repository: ApplicantRepositoryAdapter):
        self.repository = repository

    async def create(self, applicant: Applicant) -> None:
        await self.repository.save(applicant.email, applicant.password)

    async def patch(self, email: str, patch_data: Applicant) -> None:
        await self.repository.patch(email, patch_data)

    async def delete(self, email: str) -> None:
        await self.repository.delete(email)

    async def get_list(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Applicant]:
        applicants = await self.repository.get_list(filters)
        return applicants

    async def get_one(self, email: str) -> Applicant:
        applicant = await self.repository.get_one(email)
        return applicant
