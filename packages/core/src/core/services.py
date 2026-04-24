"""Business logic for selecting and retrieving issue digests."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from core.config import CoreConfig
from core.errors import InvalidIssueRequestError, IssueNotFoundError
from core.models import DigestRequest, Issue, IssueDigest, IssueStatus
from core.protocols import IssueSource


@dataclass(slots=True, frozen=True)
class InMemoryIssueSource:
    issues: tuple[Issue, ...]

    def list_issues(self) -> tuple[Issue, ...]:
        return self.issues


class IssueDigestService:
    def __init__(self, source: IssueSource, config: CoreConfig | None = None) -> None:
        self.source = source
        self.config = config or CoreConfig()

    def list_issues(self, request: DigestRequest | None = None) -> IssueDigest:
        resolved_request = self._normalize_request(request)
        items = list(self.source.list_issues())
        filtered = [
            issue
            for issue in items
            if self._matches_status(issue, resolved_request.status)
            and self._matches_assignee(issue, resolved_request.assignee)
            and issue.matches_search(resolved_request.search)
            and self._matches_label(issue, resolved_request.label)
        ]
        filtered.sort(key=_sort_key, reverse=True)

        start = (resolved_request.page - 1) * resolved_request.limit
        end = start + resolved_request.limit
        limited = tuple(filtered[start:end])
        return IssueDigest(request=resolved_request, total=len(filtered), items=limited)

    def get_issue(self, issue_id: str) -> Issue:
        for issue in self.source.list_issues():
            if issue.id == issue_id:
                return issue
        raise IssueNotFoundError(issue_id)

    def _normalize_request(self, request: DigestRequest | None) -> DigestRequest:
        resolved = request or DigestRequest(limit=self.config.default_limit)
        if resolved.limit <= 0:
            raise InvalidIssueRequestError("limit must be greater than zero")
        if resolved.page <= 0:
            raise InvalidIssueRequestError("page must be greater than zero")

        return resolved

    @staticmethod
    def _matches_status(issue: Issue, status: IssueStatus | None) -> bool:
        return status is None or issue.status is status

    @staticmethod
    def _matches_assignee(issue: Issue, assignee: str | None) -> bool:
        if assignee is None:
            return True
        return (issue.assignee or "").casefold() == assignee.casefold()

    @staticmethod
    def _matches_label(issue: Issue, label: str | None) -> bool:
        if label is None:
            return True
        return any(existing_label.casefold() == label.casefold() for existing_label in issue.labels)


def build_demo_service(config: CoreConfig | None = None) -> IssueDigestService:
    resolved_config = config or CoreConfig()
    source = InMemoryIssueSource(issues=_demo_issues(resolved_config.source_name))
    return IssueDigestService(source=source, config=resolved_config)


def _demo_issues(source_name: str) -> tuple[Issue, ...]:
    return (
        Issue(
            id="ISS-101",
            title="Retry failed digest fetches when upstream rate limits",
            status=IssueStatus.OPEN,
            summary=("The hourly digest job drops updates instead of backing off when the source API returns 429."),
            assignee="alex",
            labels=("reliability", "backend"),
            source=source_name,
            url="https://issues.example.local/ISS-101",
            created_at=_dt(2026, 3, 21, 13, 30),
            updated_at=_dt(2026, 3, 29, 9, 15),
        ),
        Issue(
            id="ISS-102",
            title="Normalize label casing before rendering summaries",
            status=IssueStatus.IN_PROGRESS,
            summary=(
                "Some imported tickets arrive as BUG while others arrive as bug, which leaks into the CLI output."
            ),
            assignee="sam",
            labels=("data-shape", "cli"),
            source=source_name,
            url="https://issues.example.local/ISS-102",
            created_at=_dt(2026, 3, 18, 8, 45),
            updated_at=_dt(2026, 3, 28, 16, 0),
        ),
        Issue(
            id="ISS-103",
            title="Document local API workflow for the team",
            status=IssueStatus.CLOSED,
            summary=(
                "The service is fine, but new contributors keep missing the uv commands needed to boot it locally."
            ),
            assignee=None,
            labels=("docs",),
            source=source_name,
            url="https://issues.example.local/ISS-103",
            created_at=_dt(2026, 3, 10, 10, 0),
            updated_at=_dt(2026, 3, 23, 11, 30),
        ),
        Issue(
            id="ISS-104",
            title="Support assignee filters in the digest service",
            status=IssueStatus.OPEN,
            summary="Product wants one digest per engineer instead of a single combined report.",
            assignee="alex",
            labels=("feature", "api"),
            source=source_name,
            url="https://issues.example.local/ISS-104",
            created_at=_dt(2026, 3, 22, 14, 0),
            updated_at=_dt(2026, 3, 27, 14, 15),
        ),
        Issue(
            id="ISS-105",
            title="Move the sample source behind an HTTP-backed repository",
            status=IssueStatus.OPEN,
            summary=(
                "The in-memory source is deliberate for now, but the next step is "
                "swapping in a real integration boundary."
            ),
            assignee="jordan",
            labels=("integration", "todo"),
            source=source_name,
            url="https://issues.example.local/ISS-105",
            created_at=_dt(2026, 3, 25, 9, 0),
            updated_at=_dt(2026, 3, 29, 11, 45),
        ),
        Issue(
            id="ISS-106",
            title="Investigate support for blocked status in the digest",
            status=IssueStatus.BLOCKED,
            summary=(
                "Some issues are blocked by external dependencies and can't be resolved until those are "
                "addressed. It would be nice to track those separately instead of lumping them in with "
                "open work."
            ),
            assignee=None,
            labels=("research",),
            source=source_name,
            url="https://issues.example.local/ISS-106",
            created_at=_dt(2026, 3, 26, 10, 30),
            updated_at=_dt(2026, 3, 29, 12, 0),
        ),
    )


def _dt(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=UTC)


def _sort_key(issue: Issue) -> tuple[datetime, datetime, str]:
    return issue.updated_at, issue.created_at, issue.id
