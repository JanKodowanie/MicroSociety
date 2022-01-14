import sys
import uvicorn
import asyncio
import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from common.ms_app import MSApp
from core.events.event_handler import EventHandler


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
    uvicorn.run('main:app', host="0.0.0.0", port=8003, reload=True)