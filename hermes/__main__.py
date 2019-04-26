import asyncio
import uvloop

from hermes.presentation.app import create_app
from hermes.misc.config import settings


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = create_app()

    app.run(
        host=settings.RUN_HOST,
        port=settings.RUN_PORT,
        debug=settings.DEBUG
    )
