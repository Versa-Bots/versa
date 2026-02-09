import asyncio
import io
import time
from pathlib import Path

import discord
from discord import ClientUser, option, slash_command
from PIL import Image, UnidentifiedImageError

MAX_IMAGE_FILESIZE = 50_000_000  # 50 MB
SUPPORTED_IMAGE_FORMATS = {"jpeg", "png", "gif", "webp", "tiff", "bmp"}
TRANSPARENT_FORMATS = {"png", "webp", "tiff"}


class SlashCommands(discord.Cog, name="slash_commands"):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.started_time = time.time()

    @slash_command()
    async def info(self, ctx: discord.ApplicationContext) -> None:
        """Display information about the bot."""
        assert self.bot.user is not None
        bot_user: ClientUser = self.bot.user
        container = discord.ui.Container()
        container.add_section(
            discord.ui.TextDisplay(f"""
{bot_user.name} is a bot developed by [Versa Bots](https://github.com/Versa-Bots/) offering utility commands.
**Users:** {len(self.bot.users)}
**Servers:** {len(self.bot.guilds)}
**API Latency:** {round(self.bot.latency * 1000)}ms
**Pycord Version:** {discord.__version__}
**Uptime:** {self.format_uptime(time.time() - self.started_time)}
**Code:** https://github.com/Versa-Bots/versa/"""),
            accessory=discord.ui.Thumbnail(url=bot_user.display_avatar.url),
        )
        inv_button_row = discord.ui.ActionRow(
            discord.ui.Button(label="Invite", url=f"https://discord.com/api/oauth2/authorize?client_id={bot_user.id}")
        )
        await ctx.respond(view=discord.ui.DesignerView(container, inv_button_row))

    @slash_command()
    @option("image", discord.Attachment, description="The image to convert")
    @option(
        "target_filetype",
        description="The filetype to convert to",
        choices=SUPPORTED_IMAGE_FORMATS,
    )
    async def convert(
        self,
        ctx: discord.ApplicationContext,
        image: discord.Attachment,
        target_filetype: str,
    ) -> None:
        """Convert an image to another image format. Animated GIFs will be converted to static images."""
        if not image.content_type or not image.content_type.startswith("image/"):
            await ctx.respond("Attached file is not an image!", ephemeral=True)
            return
        if image.size > MAX_IMAGE_FILESIZE:
            await ctx.respond(
                f"Attached file is too large! Keep it below {MAX_IMAGE_FILESIZE // 1_000_000}MB.", ephemeral=True
            )
            return

        await ctx.defer(ephemeral=True)
        file_bytes = await image.read()
        try:
            converted = await asyncio.get_running_loop().run_in_executor(
                None, self.convert_image, file_bytes, target_filetype
            )
        except (FileNotFoundError, UnidentifiedImageError):
            await ctx.respond("Something went wrong", ephemeral=True)
            return

        await ctx.respond(
            file=discord.File(converted, filename=self.replace_extension(image.filename, target_filetype)),
            ephemeral=True,
        )

    @staticmethod
    def replace_extension(filename: str, new_extension: str) -> str:
        """Replace the file extension of a filename with the given one.

        :param filename: The filename to replace the extension of
        :param new_extension: The extension to replace the old one with

        :return str: The new filename with the new extension
        """
        return Path(filename).stem + "." + new_extension

    @staticmethod
    def convert_image(image_bytes: bytes, target_filetype: str) -> io.BytesIO:
        """Convert given image bytes to other image formats.

        :param image_bytes: The image bytes to convert
        :param target_filetype: The filetype to convert to

        :return BytesIO: The converted image bytes
        """
        file = io.BytesIO(image_bytes)
        buffer = io.BytesIO()
        with Image.open(file) as image:
            if target_filetype not in TRANSPARENT_FORMATS and image.mode != "RGB":
                image.convert("RGB").save(
                    buffer, format=target_filetype
                )  # Cut the alpha channel to support PNG / WebP / TIFF -> X
            else:
                image.save(buffer, format=target_filetype)

        buffer.seek(0)
        return buffer

    @staticmethod
    def format_uptime(seconds: float) -> str:
        seconds = int(seconds)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")

        return " ".join(parts)


def setup(bot: discord.Bot) -> None:
    bot.add_cog(SlashCommands(bot))
