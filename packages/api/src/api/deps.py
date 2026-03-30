"""Dependency wiring for the FastAPI package."""

from __future__ import annotations

from typing import Annotated

from core import CoreConfig, IssueDigestService, build_demo_service
from fastapi import Depends


def get_core_config() -> CoreConfig:
    return CoreConfig.from_env()


def get_issue_service(
    config: Annotated[CoreConfig, Depends(get_core_config)],
) -> IssueDigestService:
    return build_demo_service(config)


CoreConfigDep = Annotated[CoreConfig, Depends(get_core_config)]
IssueServiceDep = Annotated[IssueDigestService, Depends(get_issue_service)]
