"""Local item commands backed by the shared core package."""

from __future__ import annotations

from core import (
    DigestRequest,
    Issue,
    IssueDigest,
    IssueDigestService,
    IssueStatus,
    build_demo_service,
)


def list_items(
    *,
    status: IssueStatus | None,
    assignee: str | None,
    search: str | None,
    limit: int | None,
    service: IssueDigestService | None = None,
) -> IssueDigest:
    current_service = service or build_demo_service()
    request = DigestRequest(
        status=status,
        assignee=assignee,
        search=search,
        limit=limit or current_service.config.default_limit,
    )
    return current_service.list_issues(request)


def show_item(issue_id: str, *, service: IssueDigestService | None = None) -> Issue:
    current_service = service or build_demo_service()
    return current_service.get_issue(issue_id)


# TODO: Add an `items export` subcommand that writes the digest to disk for cron-style workflows.
