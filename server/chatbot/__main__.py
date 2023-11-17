import uvicorn

from chatbot.settings import settings
from dotenv import load_dotenv

def main() -> None:
    """Entrypoint of the application."""
    load_dotenv()
    uvicorn.run(
        "chatbot.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
