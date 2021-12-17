import uvicorn
import settings
import asyncio
import sys
from fastapi.staticfiles import StaticFiles
from common.ms_app import MSApp
from core.accounts.router import router as accounts_router
from core.blog_users.router import router as blog_users_router
from core.employees.router import router as employees_router
from core.events.event_handler import EventHandler
from feed_db import feed_db


app = MSApp()
app.include_router(accounts_router)
app.include_router(blog_users_router)
app.include_router(employees_router)
app.mount(settings.MEDIA_ROOT, StaticFiles(directory=settings.MEDIA_DIR), name="media")


try:
    settings.create_db_connection(app)
except Exception as e:
    settings.logger.error("Couldn't connect to db")
    settings.logger.error(e)
    sys.exit(-1)


@app.on_event('startup')
async def startup():
    await feed_db()
    loop = asyncio.get_running_loop()
    await app.broker_client.initialize(loop, EventHandler.handle_events)
    task = loop.create_task(app.broker_client.consume())
    await task


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)