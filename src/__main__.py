import asyncio
import logging

import discord

from src import log_setup
from src.database import init_db, shutdown_db

from .config import TOKEN

log_setup.setup_logging(logging.INFO)
logger = logging.getLogger(__name__)

bot = discord.Bot(
    intents=discord.Intents.default(),
    default_command_integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install},
)

bot.load_extensions("src.cogs")
logger.info("Loaded cogs: %s", ", ".join(bot.cogs))


@bot.listen()
async def on_connect() -> None:
    logger.info("Connected to Discord!")


@bot.listen()
async def on_ready() -> None:
    logger.info("Logged in as %s", bot.user)
    logger.info("----------------------------")


async def start() -> None:
    original_exc = None
    try:
        await init_db()
        async with bot:
            await bot.start(TOKEN)
    except Exception as e:  # noqa: BLE001
        original_exc = e
    finally:
        try:
            await shutdown_db()
        except Exception as e2:
            if original_exc:
                msg = "Multiple errors happened when starting the bot"

                raise ExceptionGroup(msg, [original_exc, e2]) from None
            raise
        if original_exc:
            raise original_exc


if __name__ == "__main__":
    asyncio.run(start())
