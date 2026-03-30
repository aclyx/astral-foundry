"""Health route definitions."""

from __future__ import annotations

from fastapi import APIRouter

from api.deps import CoreConfigDep

router = APIRouter(tags=["health"])


@router.get("/health")
def read_health(config: CoreConfigDep) -> dict[str, object]:
    return {
        "status": "ok",
        "service": "astral-foundry-api",
        "default_limit": config.default_limit,
        "source_name": config.source_name,
    }
