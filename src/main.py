from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {
        "status": "healthy",
        "message": "Sports Spoiler Detector API"
    }