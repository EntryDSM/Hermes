from user.connection import MySQLConnection
from user.cache import Cache
from user.model import Admin, Applicant, ApplicantStatus


async def initialize(app, roop):
    await MySQLConnection.initialize()
    await Cache.initialize()

    await Admin.create_table()
    await Applicant.create_table()
    await ApplicantStatus.create_table()
    # enable for production


async def destroy(app, loop):
    await MySQLConnection.destroy()
    await Cache.destroy()
