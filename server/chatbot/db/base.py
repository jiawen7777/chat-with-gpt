from sqlalchemy.orm import DeclarativeBase

from chatbot.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
