import logging

import discord

from src.config import HEALTHCHECK_HOST, HEALTHCHECK_PORT_RAW
from src.runtime_healthcheck import HealthcheckServer

logger = logging.getLogger(__name__)
HEALTHCHECK_COG_NAME = "healthcheck"


class HealthcheckCog(discord.Cog, name=HEALTHCHECK_COG_NAME):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot: discord.Bot = bot
        self.healthcheck_server: HealthcheckServer | None = None
        if HEALTHCHECK_HOST:
            if HEALTHCHECK_PORT_RAW is None:
                msg = (
                    "Environment variable HEALTHCHECK_PORT must be set to a valid integer when "
                    "HEALTHCHECK_HOST is configured "
                    f"(HEALTHCHECK_HOST={HEALTHCHECK_HOST}, HEALTHCHECK_PORT={HEALTHCHECK_PORT_RAW})"
                )
                raise RuntimeError(msg)

            try:
                healthcheck_port = int(HEALTHCHECK_PORT_RAW)
            except ValueError as e:
                msg = (
                    "Environment variable HEALTHCHECK_PORT must be set to a valid integer when "
                    "HEALTHCHECK_HOST is configured "
                    f"(HEALTHCHECK_HOST={HEALTHCHECK_HOST}, HEALTHCHECK_PORT={HEALTHCHECK_PORT_RAW})"
                )
                raise RuntimeError(msg) from e

            self.healthcheck_server = HealthcheckServer(
                bot,
                host=HEALTHCHECK_HOST,
                port=healthcheck_port,
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
