from hermes.adapters.repositories.applicant_status import (
    ApplicantStatusRepositoryAdapter,
)
from hermes.entities.applicant_status import ApplicantStatus


class ApplicantStatusService:
    def __init__(self, repository: ApplicantStatusRepositoryAdapter):
        self.repository = repository

    async def init(self, email: str) -> None:
        await self.repository.init(email)

    async def patch(self, email: str, patch_data: ApplicantStatus) -> None:
        await self.repository.patch(email, patch_data)

    async def get_one(self, email: str) -> ApplicantStatus:
        status = await self.repository.get_one(email)
        return status
