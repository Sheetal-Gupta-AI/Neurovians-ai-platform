import logging
from contextlib import asynccontextmanager
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from psycopg_pool import ConnectionPool

from app.config import get_settings
from app.controller import router as model_router
from app.model_registry import ModelRegistry


APP_DIRECTORY = Path(__file__).parent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    connection_pool = ConnectionPool(
        conninfo=settings.database_url,
        open=True,
    )

    app.state.model_registry = ModelRegistry(
        connection_pool=connection_pool,
        organization_id=str(settings.demo_organization_id),
    )

    yield

    connection_pool.close()


app = FastAPI(
    title="Neurovians AI Gateway",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(model_router)


@app.middleware("http")
async def log_request(request: Request, call_next):
    trace_id = request.headers.get("x-trace-id") or str(uuid4())
    started_at = perf_counter()

    response = await call_next(request)
    response.headers["x-trace-id"] = trace_id

    logger.info(
        "request_completed trace_id=%s method=%s path=%s status=%s duration_ms=%s",
        trace_id,
        request.method,
        request.url.path,
        response.status_code,
        round((perf_counter() - started_at) * 1000, 2),
    )

    return response


@app.get("/", include_in_schema=False)
def ui() -> FileResponse:
    return FileResponse(APP_DIRECTORY / "static" / "index.html")