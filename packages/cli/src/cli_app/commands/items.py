"""Local item commands backed by the shared core package."""

from __future__ import annotations

from pathlib import Path

from core import (
    DigestRequest,
    Issue,
    IssueDigest,
    IssueDigestService,
    IssueStatus,
    build_demo_service,
)

from cli_app.output import emit


def list_items(
    *,
    status: IssueStatus | None,
    assignee: str | None,
    search: str | None,
    limit: int | None,
    service: IssueDigestService | None = None,
    label: str | None = None,
) -> IssueDigest:
    current_service = service or build_demo_service()
    request = DigestRequest(
        status=status,
        assignee=assignee,
        search=search,
        label=label,
        limit=limit or current_service.config.default_limit,
    )
    return current_service.list_issues(request)


def show_item(issue_id: str, *, service: IssueDigestService | None = None) -> Issue:
    current_service = service or build_demo_service()
    return current_service.get_issue(issue_id)


def export_items(
    *,
    path: Path,
    status: IssueStatus | None,
    assignee: str | None,
    search: str | None,
    limit: int | None,
    service: IssueDigestService | None = None,
    label: str | None = None,
) -> dict[str, object]:
    current_service = service or build_demo_service()
    request = DigestRequest(
        status=status,
        assignee=assignee,
        search=search,
        label=label,
        limit=limit or current_service.config.default_limit,
    )

    digest = current_service.list_issues(request)

    with path.open("w", encoding="utf-8") as stream:
        emit(digest, output="json", stream=stream)

    return {"path": str(path), "exported": digest.returned}
