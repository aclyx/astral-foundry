"""Remote fetch behavior for the CLI package."""

from __future__ import annotations

import httpx
from core import SourceUnavailableError

from cli_app.config import CliConfig


def fetch_items(
    config: CliConfig,
    *,
    status: str | None,
    limit: int | None,
    client: httpx.Client | None = None,
) -> dict[str, object]:
    params: dict[str, str | int] = {}
    if status:
        params["status"] = status
    if limit is not None:
        params["limit"] = limit

    close_client = client is None
    current_client = client or httpx.Client(timeout=config.timeout_seconds)
    try:
        response = current_client.get(f"{config.api_base_url}/items", params=params)
        response.raise_for_status()
        return dict(response.json())
    except httpx.HTTPError as exc:
        raise SourceUnavailableError(f"could not fetch items from {config.api_base_url!r}") from exc
    finally:
        if close_client:
            current_client.close()


# TODO: Replace the plain timeout with a richer httpx.Timeout setup
# when you point this at a real API.
