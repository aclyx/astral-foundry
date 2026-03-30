"""Application entrypoint for the FastAPI package."""

from __future__ import annotations

from fastapi import FastAPI

from api.config import ApiConfig
from api.routers import health, items


def create_app(config: ApiConfig | None = None) -> FastAPI:
    resolved_config = config or ApiConfig.from_env()
    app = FastAPI(
        title="Astral Foundry API",
        version="0.1.0",
        debug=resolved_config.debug,
        description="HTTP interface for the developer issue digest workspace.",
    )
    app.state.api_config = resolved_config
    app.include_router(health.router)
    app.include_router(items.router)
    return app


app = create_app()
