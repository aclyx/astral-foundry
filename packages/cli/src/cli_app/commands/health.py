"""Health-related CLI behavior."""

from __future__ import annotations

import httpx
from core import SourceUnavailableError, build_demo_service

from cli_app.config import CliConfig


def build_health_report(
    config: CliConfig,
    *,
    remote: bool,
    client: httpx.Client | None = None,
) -> dict[str, object]:
    service = build_demo_service()
    local_digest = service.list_issues()
    report: dict[str, object] = {
        "status": "ok",
        "api_base_url": config.api_base_url,
        "default_output": config.default_output,
        "local_issue_count": local_digest.total,
        "config_path": str(config.config_path) if config.config_path else None,
    }

    if remote:
        report["remote"] = _fetch_remote_health(config, client=client)
    return report


def _fetch_remote_health(
    config: CliConfig, *, client: httpx.Client | None = None
) -> dict[str, object]:
    close_client = client is None
    current_client = client or httpx.Client(timeout=config.timeout_seconds)
    try:
        response = current_client.get(f"{config.api_base_url}/health")
        response.raise_for_status()
        return dict(response.json())
    except httpx.HTTPError as exc:
        raise SourceUnavailableError(
            f"could not reach the API health endpoint at {config.api_base_url!r}",
        ) from exc
    finally:
        if close_client:
            current_client.close()
