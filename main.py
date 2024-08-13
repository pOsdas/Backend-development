import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_v1_router, prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {
        "message": "Hello"
    }


@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello, {name}!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
