"""Pydantic schemas for item responses."""

from __future__ import annotations

from datetime import datetime

from core import Issue, IssueStatus
from pydantic import BaseModel, ConfigDict


class IssueRead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    status: IssueStatus
    summary: str
    assignee: str | None
    labels: list[str]
    source: str
    url: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, issue: Issue) -> IssueRead:
        return cls(
            id=issue.id,
            title=issue.title,
            status=issue.status,
            summary=issue.summary,
            assignee=issue.assignee,
            labels=list(issue.labels),
            source=issue.source,
            url=issue.url,
            created_at=issue.created_at,
            updated_at=issue.updated_at,
        )


class ItemListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total: int
    returned: int
    items: list[IssueRead]
