"""
The App Entrypoint
This wires everything together:

- Include your routers
- Set up middleware
- Launch the app

Nothing else should live here.

Ref: https://medium.com/the-pythonworld/the-architecture-blueprint-every-python-backend-project-needs-207216931123
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {
        "status": "healthy",
        "message": "Sports Spoiler Detector API"
    }