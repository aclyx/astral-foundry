"""Issue item route definitions."""

from __future__ import annotations

from typing import Annotated

from core import IssueNotFoundError, IssueStatus
from fastapi import APIRouter, HTTPException, Query

from api.deps import IssueServiceDep
from api.schemas.items import IssueRead, ItemListResponse
from api.services.items import get_item, list_items

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=ItemListResponse)
def read_items(
    service: IssueServiceDep,
    status: Annotated[IssueStatus | None, Query()] = None,
    assignee: Annotated[str | None, Query(max_length=100)] = None,
    search: Annotated[str | None, Query(max_length=100)] = None,
    limit: Annotated[int | None, Query(ge=1, le=100)] = None,
    label: Annotated[str | None, Query(max_length=50)] = None,
) -> ItemListResponse:
    return list_items(
        service,
        status=status,
        assignee=assignee,
        search=search,
        limit=limit,
        label=label,
    )


@router.get("/{item_id}", response_model=IssueRead)
def read_item(item_id: str, service: IssueServiceDep) -> IssueRead:
    try:
        return get_item(service, item_id)
    except IssueNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


# TODO: Add page or cursor parameters once the list view needs stable pagination semantics.
