from typing import cast

import httpx
import pytest
from cli_app.commands.fetch import fetch_items
from cli_app.config import CliConfig
from core.errors import SourceUnavailableError


def test_fetch_items_uses_httpx_and_returns_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["status"] == "open"
        return httpx.Response(
            200,
            json={
                "total": 1,
                "returned": 1,
                "items": [
                    {
                        "id": "ISS-101",
                        "title": "Retry failed digest fetches when upstream rate limits",
                        "status": "open",
                    },
                ],
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://testserver")
    payload = fetch_items(
        CliConfig(api_base_url="http://testserver"),
        status="open",
        limit=5,
        client=client,
    )

    assert payload["returned"] == 1
    items = cast(list[dict[str, object]], payload["items"])
    assert items[0]["id"] == "ISS-101"


def test_fetch_with_assignee_and_search_and_label() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["assignee"] == "alice"
        assert request.url.params["search"] == "bug"
        assert request.url.params["label"] == "high-priority"
        return httpx.Response(200, json={"total": 0, "returned": 0, "items": []})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://testserver")
    payload = fetch_items(
        CliConfig(api_base_url="http://testserver"),
        status=None,
        page=None,
        limit=None,
        assignee="alice",
        search="bug",
        label="high-priority",
        client=client,
    )

    assert payload["returned"] == 0


def test_fetch_items_wraps_http_errors() -> None:
    client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(503, request=request)),
        base_url="http://testserver",
    )

    with pytest.raises(SourceUnavailableError):
        fetch_items(CliConfig(api_base_url="http://testserver"), status=None, limit=None, client=client)


def test_fetch_items_wraps_timeout_errors() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timed out", request=request)

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://testserver",
    )

    with pytest.raises(SourceUnavailableError, match="timed out"):
        fetch_items(CliConfig(api_base_url="http://testserver"), status=None, limit=None, client=client)
