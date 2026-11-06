from fastapi import FastAPI

app = FastAPI(
    title="AI Voice Assistant",
    description="My Personal AI Voice Assistant Backend",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Voice Assistant!"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }