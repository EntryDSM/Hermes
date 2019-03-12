from hermes.connection import MySQLConnection
from hermes.cache import Cache
from hermes.model import Admin, Applicant, ApplicantStatus


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
