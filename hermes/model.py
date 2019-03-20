from typing import Dict, Union, Iterable, Tuple, List

from hermes.connection import MySQLConnection
from hermes.descriptor import *


class BaseModel:
    table_name: str
    indexes: Dict[str, Union[str, Tuple]]

    table_creation_statement: str

    @classmethod
    async def create_table(cls):
        await MySQLConnection.execute(cls.table_creation_statement)
        await cls.create_table_index()

    @classmethod
    async def create_table_index(cls):
        for index_name, index_key in cls.indexes.items():
            try:
                await MySQLConnection.execute(f"CREATE INDEX {index_name} ON {cls.table_name} ({', '.join(str(i) for i in index_key)})")
            except Exception as e:
                if e.args[0] == 1061:
                    pass

    async def save(self):
        pass


class Admin(BaseModel):
    table_name = "admin"
    indexes = {
        "type_index": ("admin_type", ),
        "name_index": ("admin_name", ),
    }

    table_creation_statement = f"""
        create table if not exists {table_name}
            (
              admin_id       varchar(45)                                  not null
                primary key,
              admin_password varchar(320)                                  not null,
              admin_type     enum ('ROOT', 'ADMINISTRATION', 'INTERVIEW') not null,
              admin_email    varchar(320)                                 not null,
              admin_name     varchar(13)                                  not null,
              created_at     timestamp default CURRENT_TIMESTAMP          not null,
              updated_at     timestamp default CURRENT_TIMESTAMP          not null
            ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;
    """

    json: Dict[str, str]

    admin_id = String(length=45, allow_none=False)
    admin_password = Password(allow_none=False)
    admin_type = AdminEnum(allow_none=False)
    admin_email = Email(allow_none=False)
    admin_name = String(length=13, allow_none=False)
    created_at = TimeStamp(default=datetime.datetime.now, allow_none=False)
    updated_at = TimeStamp(default=datetime.datetime.now, allow_none=False)

    def __init__(self, admin_id, admin_name, admin_email, admin_password, admin_type, created_at=None, updated_at=None):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.admin_type = admin_type

        if created_at and updated_at:
            self.created_at = created_at
            self.updated_at = updated_at

        self.json: Dict = {
            "id": self.admin_id,
            "name": self.admin_name,
            "email": self.admin_email,
            "type": self.admin_type
        }

    async def save(self) -> None:
        query = f"""INSERT INTO {self.table_name} (
                    admin_id,
                    admin_password,
                    admin_type,
                    admin_email,
                    admin_name,
                    created_at,
                    updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        await MySQLConnection.execute(
            query, self.admin_id,
            generate_password_hash(self.admin_password),
            self.admin_type,
            self.admin_email,
            self.admin_name,
            self.created_at,
            self.updated_at
        )

    async def update_info(self) -> None:
        query = f"""
        UPDATE {self.table_name}
        SET admin_email = %s,
            admin_type = %s,
            admin_name = %s,
            updated_at = %s
        WHERE
            admin_id = %s
        """

        await MySQLConnection.execute(
            query,
            self.admin_email,
            self.admin_type,
            self.admin_name,
            datetime.datetime.now(),
            self.admin_id
        )

    async def update_password(self) -> None:
        query = f"""
        UPDATE {self.table_name}
        SET admin_password = %s,
            updated_at = %s
        WHERE
            admin_id = %s
        """
        await MySQLConnection.execute(
            query,
            self.admin_password,
            datetime.datetime.now()
        )

    async def delete(self) -> None:
        query = f"""
        DELETE FROM {self.table_name} WHERE admin_id = %s
        """
        await MySQLConnection.execute(query, self.admin_id)

    @classmethod
    async def query_by_email(cls, email: str) -> "Admin":
        query = f"""
                SELECT *
                FROM {cls.table_name}
                WHERE admin_email = %s
                """

        result = await MySQLConnection.fetchone(query, email)
        return Admin(**result) if result else None

    @classmethod
    async def query_by_id(cls, admin_id: str) -> "Admin":
        query = f"""
                SELECT *
                FROM {cls.table_name}
                WHERE admin_id = %s
                """

        result = await MySQLConnection.fetchone(query, admin_id)
        return Admin(**result) if result else None

    @classmethod
    async def query_by_name(cls, name: str) -> "Admin":
        query = f"""
        SELECT *
        FROM {cls.table_name}
        WHERE admin_name = %s
        """

        result = await MySQLConnection.fetchone(query, name)
        return Admin(**result) if result else None

    @classmethod
    async def query(cls, **kwargs) -> List["Admin"]:
        base_query = f"""
        SELECT *
        FROM {cls.table_name}\n
        """

        if kwargs:
            base_query += "WHERE"
            for k in kwargs.keys():
                base_query += f" {k} = %s AND"
            base_query = f"{base_query[:-3]};"

        result = await MySQLConnection.fetch(base_query, *kwargs.values())

        return [Admin(**r) for r in result] if result else None

    @classmethod
    async def get_type(cls, email: str) -> "Admin":
        query = f"""
                SELECT *
                FROM {cls.table_name}
                WHERE admin_email = %s
                """

        result = await MySQLConnection.fetchone(query, email)
        return result["admin_type"] if result else None


class Applicant(BaseModel):
    table_name = "applicant"
    indexes = {}

    table_creation_statement = f"""
    create table if not exists {table_name}
    (
      email          varchar(320)                        not null
        primary key,
      password       varchar(320)                        not null,
      applicant_name varchar(13)                         null,
      sex            enum ('MALE', 'FEMALE')             null,
      birth_date     date                                null,
      parent_name    varchar(13)                         null,
      parent_tel     varchar(12)                         null,
      applicant_tel  varchar(12)                         null,
      address        varchar(500)                        null,
      post_code      varchar(5)                          null,
      image_path     varchar(256)                        null,
      created_at     timestamp default CURRENT_TIMESTAMP not null,
      updated_at     timestamp default CURRENT_TIMESTAMP not null,
      constraint applicant_tel_UNIQUE
        unique (applicant_tel),
      constraint image_path_UNIQUE
        unique (image_path)
    );
    """

    email = Email(allow_none=False)
    password = String(length=320, allow_none=False)
    applicant_name = String(length=13)
    sex = SexEnum()
    birth_date = Date()
    parent_name = String(length=13)
    parent_tel = PhoneNumber()
    applicant_tel = PhoneNumber()
    address = String(length=500)
    post_code = String(length=5)
    image_path = String(length=256)
    created_at = TimeStamp(default=datetime.datetime.now, allow_none=False)
    updated_at = TimeStamp(default=datetime.datetime.now, allow_none=False)

    def __init__(self, email, password, applicant_name=None, sex=None, birth_date=None, parent_name=None,
                 parent_tel=None, applicant_tel=None, address=None, post_code=None, image_path=None,
                 created_at=None, updated_at=None):
        self.email = email
        self.password = password
        self.applicant_name = applicant_name
        self.sex = sex
        self.birth_date = birth_date
        self.parent_name = parent_name
        self.parent_tel = parent_tel
        self.applicant_tel = applicant_tel
        self.address = address,
        self.post_code = post_code,
        self.image_path = image_path,

        if created_at and updated_at:
            self.created_at = created_at
            self.updated_at = updated_at

    async def save(self) -> None:
        query = f"""
        INSERT INTO {self.table_name} (
            email,
            password,
            applicant_name,
            sex,
            birth_date,
            parent_name,
            parent_tel,
            applicant_tel,
            address,
            post_code,
            image_path,
            created_at,
            updated_at,
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        await MySQLConnection.execute(
            query,
            self.email,
            generate_password_hash(self.password),
            self.applicant_name,
            self.sex,
            self.birth_date,
            self.parent_name,
            self.parent_tel,
            self.applicant_tel,
            self.address,
            self.post_code,
            self.image_path,
            self.created_at,
            self.updated_at
        )

    async def update_info(self) -> None:
        query = f"""UPDATE {self.table_name} 
            SET applicant_name = %s,
                sex = %s,
                birth_date = %s,
                parent_name = %s,
                parent_tel = %s,
                applicant_tel = %s,
                address = %s,
                post_code = %,
                image_path = %s,
                updated_at = %s
              WHERE email = %s
                """
        await MySQLConnection.execute(
            query,
            self.applicant_name,
            self.sex,
            self.birth_date,
            self.parent_name,
            self.parent_tel,
            self.applicant_tel,
            self.address,
            self.post_code,
            self.image_path,
            datetime.datetime.now(),
            self.email
        )

    async def change_password(self, new_password: str) -> None:
        query = f"UPDATE {self.table_name} SET password = %s, updated_at = %s WHERE email = %s"
        await MySQLConnection.execute(
            query,
            generate_password_hash(new_password),
            datetime.datetime.now(),
            self.email
        )

    @classmethod
    async def query_by_email(cls, email: str) -> "Applicant":
        query = """
        SELECT *
        FROM {cls.table_name}
        WHERE email = %s
        """

        result = await MySQLConnection.fetchone(query, email)
        return Applicant(**result) if result else None

    @classmethod
    async def query_by_name(cls, name: str) -> Iterable["Applicant"]:
        query = """
        SELECT *
        FROM {cls.table_name}
        WHERE applicant_name = %s
        """

        result = await MySQLConnection.fetch(query, name)
        return [Applicant(**r) for r in result] if result else []


class ApplicantStatus(BaseModel):
    table_name = "applicant_status"
    indexes = {}

    table_creation_statement = f"""
    create table if not exists {table_name}
    (
      applicant_email                varchar(320)                        not null
        primary key,
      receipt_code                   int(3) unsigned zerofill auto_increment,
      is_paid                        tinyint   default 0                 not null,
      is_printed_application_arrived tinyint   default 0                 not null,
      is_passed_first_apply          tinyint   default 0                 not null,
      is_final_submit                tinyint   default 0                 not null,
      exam_code                      varchar(6)                          null,
      created_at                     timestamp default CURRENT_TIMESTAMP not null,
      updated_at                     timestamp default CURRENT_TIMESTAMP not null,
      constraint exam_code_UNIQUE
        unique (exam_code),
      constraint receipt_code_UNIQUE
        unique (receipt_code),
      constraint fk_applicant_status_applicant
        foreign key (applicant_email) references applicant (email)
          on update cascade on delete cascade
    );
    """

    applicant_email = Email(allow_none=False)
    receipt_code = Integer()
    is_paid = Bool(default=False, allow_none=False)
    is_printed_application_arrived = Bool(default=False, allow_none=False)
    is_passed_first_apply = Bool(default=False, allow_none=False)
    is_final_submit = Bool(default=False, allow_none=False)
    exam_code = String(length=6)
    created_at = TimeStamp(default=datetime.datetime.now, allow_none=False)
    updated_at = TimeStamp(default=datetime.datetime.now, allow_none=False)

    def __init__(self, applicant_email, receipt_code=None, is_paid=None, is_printed_application_arrived=None,
                 is_passed_first_apply=None, is_final_submit=None, exam_code=None, created_at=None, updated_at=None):
        self.applicant_email = applicant_email
        self.receipt_code = receipt_code
        self.is_paid = is_paid
        self.is_printed_application_arrived = is_printed_application_arrived
        self.is_passed_first_apply = is_passed_first_apply
        self.is_final_submit = is_final_submit
        self.exam_code = exam_code

        if created_at and updated_at:
            self.created_at = created_at
            self.updated_at = updated_at

    async def save(self) -> None:
        query = f"INSERT INTO {self.table_name} (applicant_email) VALUES (%s)"
        await MySQLConnection.execute(query, self.applicant_email)

    async def update_paid_status(self, paid: bool) -> None:
        query = f"UPDATE {self.table_name} SET is_paid = %s, updated_at = %s WHERE applicant_email = %s"
        await MySQLConnection.execute(query, paid, datetime.datetime.now(), self.applicant_email)

    async def update_document_arrive_status(self, arrived: bool) -> None:
        query = f"UPDATE {self.table_name} SET is_printed_application_arrived = %s, updated_at = %s WHERE applicant_email = %s"
        await MySQLConnection.execute(query, arrived, datetime.datetime.now(), self.applicant_email)

    async def update_apply_result_status(self, passed: bool) -> None:
        query = f"UPDATE {self.table_name} SET is_passed_first_apply = %s, updated_at = %s WHERE applicant_email = %s"
        await MySQLConnection.execute(query, passed, datetime.datetime.now(), self.applicant_email)

    async def update_final_submit_status(self, submitted: bool) -> None:
        query = f"UPDATE {self.table_name} SET is_final_submit = %s, updated_at = %s WHERE applicant_email = %s"
        await MySQLConnection.execute(query, submitted, datetime.datetime.now(), self.applicant_email)

    async def set_exam_code(self, exam_code: str) -> None:
        query = f"UPDATE {self.table_name} SET exam_code = %s, updated_at = %s WHERE applicant_email = %s"
        await MySQLConnection.execute(query, exam_code, datetime.datetime.now(), self.applicant_email)
