from api.main import create_app
from fastapi.testclient import TestClient


def test_list_items_returns_filtered_collection() -> None:
    client = TestClient(create_app())

    response = client.get("/items", params={"status": "open", "limit": 2})

    payload = response.json()
    assert response.status_code == 200
    assert payload["returned"] == 2
    assert all(item["status"] == "open" for item in payload["items"])


def test_list_items_with_label_filter() -> None:
    client = TestClient(create_app())

    response = client.get("/items", params={"label": "api", "limit": 10})
    payload = response.json()
    assert response.status_code == 200
    assert payload["returned"] == 1
    assert payload["items"][0]["id"] == "ISS-104"


def test_get_item_returns_single_issue() -> None:
    client = TestClient(create_app())

    response = client.get("/items/ISS-101")

    assert response.status_code == 200
    assert response.json()["id"] == "ISS-101"


def test_missing_item_returns_404() -> None:
    client = TestClient(create_app())

    response = client.get("/items/ISS-404")

    assert response.status_code == 404


def test_limit_validation_returns_422() -> None:
    client = TestClient(create_app())

    response = client.get("/items", params={"limit": 0})

    assert response.status_code == 422
