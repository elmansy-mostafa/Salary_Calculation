import pytest
from fastapi.testclient import TestClient
from src.main import app  # Adjust the import based on your project structure

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
        