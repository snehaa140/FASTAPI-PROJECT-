from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_db_and_tables
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="College Lost & Found API",
    description="REST API for managing lost and found items on campus.",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "College Lost & Found API is running."
    }