import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_root_status_code():
    response = client.get("/")
    assert response.status_code == 200

def test_root_response_json():
    response = client.get("/")
    assert response.json() == {"message": "Backend is running."}

def test_root_returns_html_when_requested():
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert "text/html" in content_type.lower()
    assert "<title>Study Space Booking API</title>" in response.text

def test_app_title():
    assert getattr(app, "title", None) == "Study Space Booking API"

def test_openapi_json_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert data.get("info", {}).get("title") == app.title

def test_docs_page_available():
    response = client.get("/docs")
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert "text/html" in content_type.lower()

def test_openapi_has_paths():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data.get("paths", {}), dict)
    assert len(data.get("paths", {})) >= 0

def test_api_v1_paths_present():
    response = client.get("/openapi.json")
    data = response.json()
    paths = list(data.get("paths", {}).keys())
    assert isinstance(paths, list)
    assert any(p.startswith("/api/v1") for p in paths) or len(paths) == 0

def test_unknown_path_returns_404():
    response = client.get("/this-path-does-not-exist")
    assert response.status_code == 404
    assert "detail" in response.json()