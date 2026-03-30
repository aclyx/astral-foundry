"""Thin adapters from core services to API response models."""

from __future__ import annotations

from core import DigestRequest, IssueDigestService, IssueStatus

from api.schemas.items import IssueRead, ItemListResponse


def list_items(
    service: IssueDigestService,
    *,
    status: IssueStatus | None,
    assignee: str | None,
    search: str | None,
    limit: int | None,
) -> ItemListResponse:
    digest = service.list_issues(
        DigestRequest(
            status=status,
            assignee=assignee,
            search=search,
            limit=limit or service.config.default_limit,
        ),
    )
    return ItemListResponse(
        total=digest.total,
        returned=digest.returned,
        items=[IssueRead.from_domain(issue) for issue in digest.items],
    )


def get_item(service: IssueDigestService, item_id: str) -> IssueRead:
    return IssueRead.from_domain(service.get_issue(item_id))
