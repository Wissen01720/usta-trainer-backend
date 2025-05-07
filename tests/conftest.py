import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def client():
    from app.main import app
    with TestClient(app) as test_client:
        yield test_client