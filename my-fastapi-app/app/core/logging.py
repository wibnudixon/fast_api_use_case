import logging

from app.core.config import settings

# configures loggin along with overriding any preexisting log config
def configure_logging() -> None:
    """Configure application logging once during application startup."""
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        force=True,
    )