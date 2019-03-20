from enum import Enum
from typing import Union, NoReturn, List, Optional, Dict

from hermes.model import Admin
from hermes.exceptions import Conflict, BadRequest, NotFound
from hermes.cache import UserCache


class AdminManager:
    async def register_admin(self, admin_id: str, admin_name: str,
                             admin_email: str, admin_password: str, admin_type: Enum) -> Optional[NoReturn]:

        if await Admin.query_by_id(admin_id):
            raise Conflict("Admin already exists")

        new_admin = Admin(
            admin_id=admin_id,
            admin_name=admin_name,
            admin_email=admin_email,
            admin_password=admin_password,
            admin_type=admin_type.name
        )

        await new_admin.save()


class AdminBatchManager:
    async def search_admins(self, **kwargs) -> Union[NoReturn, List[Dict]]:

        try:
            admins = await Admin.query(**kwargs)
        except Exception:
            raise BadRequest("Invalid query")

        if not admins:
            raise NotFound("Not Found")

        return [a.json for a in admins]


class AdminInfoManager:
    async def get_admin_info(self, admin_id: str) -> Union[NoReturn, Dict]:

        admin: Union[Admin, None] = await UserCache.get(admin_id)
        if not admin:
            admin = await Admin.query_by_id(admin_id)
            if not admin:
                raise NotFound("Not Found")
            admin: Dict = admin.json
            await UserCache.set(admin_id, admin)

        return admin

    async def patch_admin_info(self, admin_id: str, **kwargs) -> None:

        admin = await Admin.query_by_id(admin_id)
        for i in kwargs.items():
            if i[1]:
                admin.__setattr__(i[0], i[1])

        await admin.update_info()

        if kwargs.get("admin_password"):
            await admin.update_password()
            # TODO: request refresh token expire to `Chanel`

        await UserCache.delete(admin_id)

    async def delete_admin(self, admin_id: str) -> None:

        admin = await Admin.query_by_id(admin_id)
        if not admin:
            raise NotFound("Not Found")
        await admin.delete()
        await UserCache.delete(admin_id)

        # TODO: request refresh token expire to `Chanel`
