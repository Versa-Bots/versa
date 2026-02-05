import io
from io import BytesIO

import discord
from discord import option, slash_command
from PIL import Image


class SlashCommands(discord.Cog, name="slash_commands"):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @slash_command()
    @option("attachment", discord.Attachment, description="The attachment to convert")
    @option(
        "target_filetype",
        description="The filetype to convert to",
        choices=["jpeg", "png", "gif", "webp", "tiff", "bmp"],
    )
    async def convert(
        self,
        ctx: discord.ApplicationContext,
        attachment: discord.Attachment,
        target_filetype: str,
    ) -> None:
        """Converts an image to another image format."""
        await ctx.defer(ephemeral=True)
        file_bytes = await attachment.read()
        converted = self.convert_image(file_bytes, target_filetype)

        await ctx.respond(
            file=discord.File(converted, filename=self.replace_extension(attachment.filename, target_filetype)),
            ephemeral=True,
        )

    @staticmethod
    def replace_extension(filename: str, new_extension: str) -> str:
        """Strip the file extension off a filename.

        :param filename: The filename to strip the extension from
        :param new_extension: The new extension to replace the old one with

        :return str: The filename without the extension and dot
        """
        return filename.rsplit(".", maxsplit=1)[0] + "." + new_extension

    @staticmethod
    def convert_image(image_bytes: bytes, target_filetype: str) -> BytesIO:
        """Converts given image bytes to other image formats.

        :param image_bytes: The image bytes to convert
        :param target_filetype: The filetype to convert to

        :return BytesIO: The converted image bytes
        """
        file = io.BytesIO(image_bytes)
        image = Image.open(file)

        image = (
            image.convert("RGBA") if target_filetype in {"png", "webp", "jxl"} else image.convert("RGB")
        )  # Cut alpha channel to support PNG / WebP -> X
        buffer = io.BytesIO()
        image.save(buffer, format=target_filetype)
        buffer.seek(0)
        return buffer


def setup(bot: discord.Bot) -> None:
    bot.add_cog(SlashCommands(bot))
