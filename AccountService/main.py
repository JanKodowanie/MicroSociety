import uvicorn
from fastapi import FastAPI
import settings
from core.accounts.router import router as accounts_router
from core.auth.router import router as auth_router


app = FastAPI()
app.include_router(accounts_router)
app.include_router(auth_router)

try:
    settings.create_db_connection(app)
except Exception:
    print("Failed to create database connection")


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)