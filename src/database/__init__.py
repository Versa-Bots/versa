import logging

import aerich
from tortoise import Tortoise

from src import config

logger = logging.getLogger(__name__)

TORTOISE_ORM = {
    "connections": {"default": f"sqlite://{config.DB_PATH}"},
    "apps": {
        "models": {
            "models": ["src.database.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}


async def init_db() -> None:
    command = aerich.Command(
        TORTOISE_ORM,
        app="models",
        location="./src/database/migrations/",
    )
    await command.init()
    migrated = await command.upgrade(run_in_transaction=True)
    if migrated:
        logger.info("Successfully migrated %s migrations: %s", len(migrated), migrated)
    else:
        logger.info("No migrations to apply.")
    await Tortoise.init(config=TORTOISE_ORM)


async def shutdown_db() -> None:
    await Tortoise.close_connections()


__all__ = ["init_db", "shutdown_db"]
