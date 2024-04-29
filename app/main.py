from typing import Union
from fastapi import FastAPI, Response, status, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import logging

from app.routers import users, drivers, trips
from app.config import POSTGRES_DATABASE_URL
from app.database import db_manager
from app.routers import background_tasks_advanced_dependencies

logging.basicConfig(filename="log.txt", level=logging.INFO)

db_manager.init(POSTGRES_DATABASE_URL)

app = FastAPI()

app.include_router(users.router)
app.include_router(drivers.router)
app.include_router(trips.router)
app.include_router(background_tasks_advanced_dependencies.router)

@app.get("/", response_class=HTMLResponse)
def root():
    return "<h1>This is the root</h1>"


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

@app.middleware("http")
async def log_request(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)
    return response