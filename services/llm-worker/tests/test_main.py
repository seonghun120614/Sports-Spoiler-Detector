"""
Make Testing a First-Class Citizen
Structure your tests to reflect your app:

```bash
/tests
├── unit/          # Isolated services, utils
├── integration/   # API + DB end-to-end tests
```

Use tools like:

- pytest
- httpx for async test clients
- pytest-asyncio for async tests

Make testing easy from day one — or you’ll never do it.

Ref: https://medium.com/the-pythonworld/the-architecture-blueprint-every-python-backend-project-needs-207216931123
"""

from fastapi.testclient import TestClient

from src.main import app

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
