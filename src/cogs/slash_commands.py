import asyncio
import io
from pathlib import Path

import discord
from discord import option, slash_command
from PIL import Image, UnidentifiedImageError

MAX_IMAGE_FILESIZE = 50_000_000


class SlashCommands(discord.Cog, name="slash_commands"):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @slash_command()
    @option("image", discord.Attachment, description="The image to convert")
    @option(
        "target_filetype",
        description="The filetype to convert to",
        choices=["jpeg", "png", "gif", "webp", "tiff", "bmp"],
    )
    async def convert(
        self,
        ctx: discord.ApplicationContext,
        image: discord.Attachment,
        target_filetype: str,
    ) -> None:
        """Converts an image to another image format. Animated GIFs will be converted to static images."""
        if not image.content_type or not image.content_type.startswith("image/"):
            await ctx.respond("Attached file is not an image!", ephemeral=True)
            return
        if image.size > MAX_IMAGE_FILESIZE:
            await ctx.respond(
                f"Attached file is too large! Keep it below {MAX_IMAGE_FILESIZE / 1_000_000}MB.", ephemeral=True
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
        """Replaces the file extension of a filename with the given one.

        :param filename: The filename to replace the extension of
        :param new_extension: The extension to replace the old one with

        :return str: The new filename with the new extension
        """
        return Path(filename).stem + "." + new_extension

    @staticmethod
    def convert_image(image_bytes: bytes, target_filetype: str) -> io.BytesIO:
        """Converts given image bytes to other image formats.

        :param image_bytes: The image bytes to convert
        :param target_filetype: The filetype to convert to

        :returns BytesIO: The converted image bytes
        """
        file = io.BytesIO(image_bytes)
        buffer = io.BytesIO()
        with Image.open(file) as image:
            if target_filetype not in {"png", "webp", "tiff"} and image.mode == "RGBA":
                image.convert("RGB").save(
                    buffer, format=target_filetype
                )  # Cut alpha channel to support PNG / WebP -> X
            else:
                image.save(buffer, format=target_filetype)

        buffer.seek(0)
        return buffer


def setup(bot: discord.Bot) -> None:
    bot.add_cog(SlashCommands(bot))
