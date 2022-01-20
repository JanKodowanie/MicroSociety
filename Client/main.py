import uvicorn
import settings
import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from core.accounts.schemas import Credentials
from core.accounts.router import router as accounts_router
from core.accounts.auth import get_refreshed_credentials, save_data_and_credentials_in_cookies
from core.blog.router import router as blog_router
from datetime import datetime, timedelta, timezone


app = FastAPI()
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

app.include_router(accounts_router)
app.include_router(blog_router)


app.mount('/static', StaticFiles(directory='static'), name="static")


@app.middleware("http")
async def refresh_credentials_if_expired(request: Request, call_next):
    credentials_cookie = request.cookies.get('credentials')
    if not credentials_cookie:
        return await call_next(request)
    credentials = Credentials(**json.loads(credentials_cookie))
    time_now = datetime.now(timezone.utc)
    updated_data = None
    if credentials.exp - time_now < timedelta(seconds=60):
            updated_data = await get_refreshed_credentials(credentials)
    response = await call_next(request)
    if updated_data:
        await save_data_and_credentials_in_cookies(updated_data, response)
    return response


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=3000, reload=True)