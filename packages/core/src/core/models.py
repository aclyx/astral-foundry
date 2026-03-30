"""Typed domain models for the issue digest workspace."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


class IssueStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


@dataclass(slots=True, frozen=True)
class Issue:
    # A dataclass is enough here: this object carries validated data and light behavior.
    id: str
    title: str
    status: IssueStatus
    summary: str
    assignee: str | None = None
    labels: tuple[str, ...] = ()
    source: str = "local-demo"
    url: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def matches_search(self, term: str | None) -> bool:
        if not term:
            return True

        query = term.casefold()
        haystacks = [
            self.id,
            self.title,
            self.summary,
            self.assignee or "",
            " ".join(self.labels),
        ]
        return any(query in value.casefold() for value in haystacks)


@dataclass(slots=True, frozen=True)
class DigestRequest:
    status: IssueStatus | None = None
    assignee: str | None = None
    search: str | None = None
    limit: int = 20


@dataclass(slots=True, frozen=True)
class IssueDigest:
    request: DigestRequest
    total: int
    items: tuple[Issue, ...]
    generated_at: datetime = field(default_factory=utc_now)

    @property
    def returned(self) -> int:
        return len(self.items)
