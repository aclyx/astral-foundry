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
    assert payload["items"][0]["id"] == "ISS-101"


def test_fetch_items_wraps_http_errors() -> None:
    client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(503, request=request)),
        base_url="http://testserver",
    )

    with pytest.raises(SourceUnavailableError):
        fetch_items(CliConfig(api_base_url="http://testserver"), status=None, limit=None, client=client)
