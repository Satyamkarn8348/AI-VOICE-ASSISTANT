
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router as main_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversation_router
from app.api.messages import router as message_router
from app.api.voice import router as voice_router
from app.api.project_builder import router as project_builder_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="My Personal AI Voice Assistant Backend"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(main_router)
app.include_router(chat_router)
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(voice_router)
app.include_router(project_builder_router)
