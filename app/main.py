from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import leads
from app.utility.logger import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    # TODO: call create_tables() here once app/database.py is implemented (TICKET-04)
    yield


app = FastAPI(title="Growth Automation Agent", version="0.1.0", lifespan=lifespan)

app.include_router(leads.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
