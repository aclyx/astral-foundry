import httpx
from cli_app.commands.health import build_health_report
from cli_app.config import CliConfig


def test_health_includes_remote_status_when_requested() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={"status": "ok", "service": "astral-foundry-api"},
        ),
    )
    client = httpx.Client(transport=transport, base_url="http://testserver")

    report = build_health_report(
        CliConfig(api_base_url="http://testserver", default_output="text"),
        remote=True,
        client=client,
    )

    assert report["status"] == "ok"
    assert report["remote"] == {"status": "ok", "service": "astral-foundry-api"}
