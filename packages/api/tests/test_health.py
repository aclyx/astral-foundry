from api.main import create_app
from fastapi.testclient import TestClient


def test_health_endpoint_reports_status() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "astral-foundry-api"
