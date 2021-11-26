import uvicorn
from fastapi import FastAPI, Depends
import settings
from core.posts.router import router as posts_router
from common.auth.jwt import JWTHandler
from common.auth.schemas import TokenDataSchema


app = FastAPI()
app.include_router(posts_router)

try:
    settings.create_db_connection(app)
except Exception:
    print("Failed to create database connection")


@app.get("/test")
async def jwt_test(user: TokenDataSchema = Depends(JWTHandler.authenticate_user)):
    return user


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8001, reload=True)