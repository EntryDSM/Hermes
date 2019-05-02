from dataclasses import dataclass


@dataclass
class Admin:
    admin_id: str
    admin_password: str
    admin_type: str
    admin_email: str
    admin_name: str
