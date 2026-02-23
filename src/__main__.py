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
    try:
        await init_db()
        async with bot:
            await bot.start(TOKEN)
    finally:
        await shutdown_db()


if __name__ == "__main__":
    asyncio.run(start())
