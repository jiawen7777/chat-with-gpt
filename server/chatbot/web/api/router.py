from fastapi.routing import APIRouter

from chatbot.web.api import echo, monitoring, chat

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
