import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

"""
Test for server loading complete
"""
def test_read_root():
    response = client.get("/")
    print(response.json())

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "message": "Sports Spoiler Detector API"
    }