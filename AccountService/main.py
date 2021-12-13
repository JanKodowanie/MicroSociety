import uvicorn
import settings
import asyncio
import sys
from common.ms_app import MSApp
# from core.accounts.router import router as accounts_router
from core.blog_users.router import router as blog_users_router
from core.employees.router import router as employees_router
# from core.auth.router import router as auth_router
from core.events.event_handler import EventHandler


app = MSApp()
# app.include_router(accounts_router)
app.include_router(blog_users_router)
app.include_router(employees_router)


try:
    settings.create_db_connection(app)
except Exception as e:
    settings.logger.error("Couldn't connect to db")
    settings.logger.error(e)
    sys.exit(-1)


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    await app.broker_client.initialize(loop, EventHandler.handle_events)
    task = loop.create_task(app.broker_client.consume())
    await task


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)