"""
The App Entrypoint
This wires everything together:

- Include your routers
- Set up middleware
- Launch the app

Nothing else should live here.

Ref: https://medium.com/the-pythonworld/the-architecture-blueprint-every-python-backend-project-needs-207216931123
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.lifespan import lifespan
from src.api.v1.endpoints.check_spoiler import router as check_spoiler_router

app = FastAPI(title="Sports Spoiler Detector API", lifespan=lifespan)
app.include_router(check_spoiler_router)

@app.get("/")
def main():
    return {
        "status": "healthy",
        "message": "Sports Spoiler Detector API"
    }
