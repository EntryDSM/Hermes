from sanic.log import logger

from hermes.misc.config import settings
from hermes.repositories.connections import MySQLConnection, RedisConnection


async def initialize(app, loop):
    database_connection_info = (
        app.database_connection_info
        if hasattr(app, "database_connection_info")
        else settings.database_connection_info
    )

    cache_connection_info = (
        app.cache_connection_info
        if hasattr(app, "cache_connection_info")
        else settings.cache_connection_info
    )

    await MySQLConnection.initialize(database_connection_info)
    await RedisConnection.initialize(cache_connection_info)

    logger.info("Connection initialize complete")


async def migrate(app, loop):
    if not MySQLConnection.is_available:
        raise Exception(
            "Database connection is unavailable, Make sure you initialize connection!"
        )

    await MySQLConnection.execute(
        """
            create table if not exists admin
            (
              admin_id       varchar(45)                                  not null
                primary key,
              admin_password varchar(100)                                 not null,
              admin_type     enum ('ROOT', 'ADMINISTRATION', 'INTERVIEW') not null,
              admin_email    varchar(320)                                 not null,
              admin_name     varchar(13)                                  not null,
              created_at     timestamp default CURRENT_TIMESTAMP          not null,
              updated_at     timestamp default CURRENT_TIMESTAMP          not null
            ) character set utf8mb4;
    """
    )
    await MySQLConnection.execute(
        """
            create table if not exists applicant
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
            ) character set utf8mb4;
        """
    )
    await MySQLConnection.execute(
        """
            create table if not exists applicant_status
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
            ) character set utf8mb4;
        """
    )

    logger.info("Database migration complete")


async def release(app, loop):
    await MySQLConnection.destroy()
    await RedisConnection.destroy()

    # All connections must be destroyed before teardown!
