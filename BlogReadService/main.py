import uvicorn
import asyncio
from common.ms_app import MSApp
from core.events.event_handler import EventHandler
from core.router import router as posts_router


app = MSApp()
app.include_router(posts_router)


@app.on_event('startup')
async def startup():
    import db
    loop = asyncio.get_running_loop()
    await app.broker_client.initialize(loop, EventHandler.handle_events)
    task = loop.create_task(app.broker_client.consume())
    await task


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8002, reload=True)