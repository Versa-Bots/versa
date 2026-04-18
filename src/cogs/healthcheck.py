import logging

import discord

from src.config import HEALTHCHECK_HOST, HEALTHCHECK_PATH, HEALTHCHECK_PORT
from src.healthcheck import HealthcheckServer

logger = logging.getLogger(__name__)
HEALTHCHECK_COG_NAME = "healthcheck"


class HealthcheckCog(discord.Cog, name=HEALTHCHECK_COG_NAME):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot: discord.Bot = bot
        self.healthcheck_server: HealthcheckServer = HealthcheckServer(
            bot,
            host=HEALTHCHECK_HOST,
            port=HEALTHCHECK_PORT,
            path=HEALTHCHECK_PATH,
        )

    @discord.Cog.listener(once=True)
    async def on_connect(self) -> None:
        await self.healthcheck_server.start()
        logger.info("Healthcheck server started from healthcheck cog")

    async def stop_server(self) -> None:
        await self.healthcheck_server.stop()


def setup(bot: discord.Bot) -> None:
    bot.add_cog(HealthcheckCog(bot))
