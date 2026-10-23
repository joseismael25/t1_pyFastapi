"""Pruebas seguras de las rutas HTTP; no insertan datos en MongoDB."""
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root_responds():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_docs_are_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
