from hermes.model import Admin
from hermes.exceptions import Conflict, BadRequest, NotFound


class AdminManager:
    async def register_admin(self, admin_id, admin_name, admin_email, admin_password, admin_type):
        if await Admin.query_by_id(admin_id):
            raise Conflict("Admin already exists")

        new_admin = Admin(admin_id=admin_id,
                          admin_name=admin_name,
                          admin_email=admin_email,
                          admin_password=admin_password,
                          admin_type=admin_type.name)
        await new_admin.save()


class AdminBatchManager:
    async def search_admins(self, **kwargs):
        admins = None

        try:
            admins = await Admin.query(**kwargs)
        except Exception as e:
            raise BadRequest("Invalid query")

        if not admins:
            raise NotFound("Not Found")

        return [a.json for a in admins]

