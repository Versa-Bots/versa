import logging
import os

import discord
from dotenv import load_dotenv

from src import log_setup

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


load_dotenv()
bot.run(os.getenv("TOKEN"))
