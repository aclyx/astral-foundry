"""Output helpers for rendering domain objects and API responses."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any, TextIO

from core.models import Issue, IssueDigest

from cli_app.config import OutputFormat


def emit(payload: Any, *, output: OutputFormat, stream: TextIO) -> None:
    if output == "json":
        json.dump(_to_json_ready(payload), stream, indent=2, sort_keys=True)
        stream.write("\n")
        return

    rendered = _render_text(payload)
    stream.write(rendered)
    if not rendered.endswith("\n"):
        stream.write("\n")


def _render_text(payload: Any) -> str:
    if isinstance(payload, IssueDigest):
        return _render_issue_rows(
            items=[_issue_to_mapping(item) for item in payload.items],
            total=payload.total,
            returned=payload.returned,
        )
    if isinstance(payload, Issue):
        return _render_issue_detail(_issue_to_mapping(payload))
    if isinstance(payload, dict) and "items" in payload and isinstance(payload["items"], list):
        return _render_issue_rows(
            items=payload["items"],
            total=int(payload.get("total", len(payload["items"]))),
            returned=int(payload.get("returned", len(payload["items"]))),
        )
    if isinstance(payload, dict) and {"id", "title", "status"} <= payload.keys():
        return _render_issue_detail(payload)
    if isinstance(payload, dict):
        return "\n".join(f"{key}: {value}" for key, value in payload.items())
    return str(payload)


def _render_issue_rows(*, items: list[dict[str, Any]], total: int, returned: int) -> str:
    lines = [f"{returned} of {total} issues"]
    for item in items:
        assignee = item.get("assignee") or "unassigned"
        lines.append(
            f"- {item['id']} [{item['status']}] {item['title']} (assignee: {assignee})",
        )
    return "\n".join(lines)


def _render_issue_detail(payload: dict[str, Any]) -> str:
    lines = [
        f"{payload['id']} [{payload['status']}]",
        payload["title"],
        "",
        f"assignee: {payload.get('assignee') or 'unassigned'}",
        f"labels: {', '.join(payload.get('labels') or []) or 'none'}",
        f"source: {payload.get('source')}",
        f"updated_at: {payload.get('updated_at')}",
        "",
        str(payload.get("summary", "")),
    ]
    return "\n".join(lines)


def _issue_to_mapping(issue: Issue) -> dict[str, Any]:
    return {
        "id": issue.id,
        "title": issue.title,
        "status": issue.status.value,
        "summary": issue.summary,
        "assignee": issue.assignee,
        "labels": list(issue.labels),
        "source": issue.source,
        "url": issue.url,
        "created_at": issue.created_at.isoformat(),
        "updated_at": issue.updated_at.isoformat(),
    }


def _to_json_ready(value: Any) -> Any:
    if isinstance(value, IssueDigest):
        return {
            "request": _to_json_ready(value.request),
            "total": value.total,
            "returned": value.returned,
            "items": [_to_json_ready(item) for item in value.items],
            "generated_at": value.generated_at.isoformat(),
        }
    if isinstance(value, Issue):
        return _issue_to_mapping(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _to_json_ready(asdict(value))
    if isinstance(value, dict):
        return {key: _to_json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_to_json_ready(item) for item in value]
    return value
