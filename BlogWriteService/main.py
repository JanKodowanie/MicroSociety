import uvicorn
import settings
import asyncio
import sys
import os
from fastapi import Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from common.ms_app import MSApp
from core.events.event_handler import EventHandler
from core.router import router as posts_router
from core.comments.router import router as comments_router


app = MSApp()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOWED_METHODS,
    allow_headers=settings.CORS_ALLOWED_HEADERS
)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS
)

app.include_router(posts_router)
app.include_router(comments_router)

try:        
    os.mkdir(settings.MEDIA_DIR)
except Exception:
    pass

app.mount(settings.MEDIA_ROOT, StaticFiles(directory=settings.MEDIA_DIR), name="media")


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
    uvicorn.run('main:app', host="0.0.0.0", port=8001, reload=True)