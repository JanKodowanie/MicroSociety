import uvicorn
import settings
import asyncio
import sys
from fastapi import Depends
from common.ms_app import MSApp
from core.events.event_handler import EventHandler
from core.posts.router import router as posts_router
from common.auth.jwt import JWTHandler
from common.auth.schemas import UserDataSchema


app = MSApp()
app.include_router(posts_router)


try:
    settings.create_db_connection(app)
except Exception as e:
    settings.logger.error("Couldn't connect to db")
    settings.logger.error(e)
    sys.exit(-1)


@app.get("/test")
async def jwt_test(user: UserDataSchema = Depends(JWTHandler.authenticate_user)):
    return user


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    await app.broker_client.initialize(loop, EventHandler.handle_events)
    task = loop.create_task(app.broker_client.consume())
    await task


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8001, reload=True)