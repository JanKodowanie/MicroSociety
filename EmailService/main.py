import uvicorn
from app import ESApp
import asyncio
from pydantic import BaseModel


app = ESApp()


class MessageSchema(BaseModel):
    message: str


@app.get('/hello')
async def hello():
    return {"message": "hello"}


@app.post('/send-message')
async def send_message(request: MessageSchema):
    await app.broker_client.send_message(
        {"message": request.message}
    )
    return {"status": "ok"}


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.broker_client.consume(loop))
    await task


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8002, reload=True)