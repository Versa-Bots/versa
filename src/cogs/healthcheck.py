import logging

import discord

from src.config import HEALTHCHECK_HOST, HEALTHCHECK_PORT
from src.runtime_healthcheck import HealthcheckServer

logger = logging.getLogger(__name__)
HEALTHCHECK_COG_NAME = "healthcheck"


class HealthcheckCog(discord.Cog, name=HEALTHCHECK_COG_NAME):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot: discord.Bot = bot
        self.healthcheck_server: HealthcheckServer | None = None
        if HEALTHCHECK_HOST:
            if HEALTHCHECK_PORT is None:
                msg = "HEALTHCHECK_PORT must be set when HEALTHCHECK_HOST is configured"
                raise RuntimeError(msg)

            self.healthcheck_server = HealthcheckServer(
                bot,
                host=HEALTHCHECK_HOST,
                port=int(HEALTHCHECK_PORT),
            )

    @discord.Cog.listener(once=True)
    async def on_connect(self) -> None:
        if self.healthcheck_server is None:
            logger.info("Healthcheck server disabled because HEALTHCHECK_HOST is unset/empty")
            return

        await self.healthcheck_server.start()
        logger.info("Healthcheck server started from healthcheck cog")

    async def stop_server(self) -> None:
        if self.healthcheck_server is None:
            return
        await self.healthcheck_server.stop()


def setup(bot: discord.Bot) -> None:
    bot.add_cog(HealthcheckCog(bot))
