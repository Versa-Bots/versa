import re

import discord
from discord import message_command


class MessageCommands(discord.Cog, name="message_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @message_command()
    async def fxlink(self, ctx: discord.ApplicationContext, message: discord.Message) -> None:
        """ Makes certain site's links embed properly within Discord """
        if not message.content:
            await ctx.respond("No link found!", ephemeral=True)
            return

        twitter_pattern = r'(https?://)(www\.)?(twitter\.com|x\.com)'
        reddit_pattern = r'(https?://)(www\.)?(reddit\.com)'
        tiktok_pattern = r'(https?://)(www\.)?((vm\.)?tiktok\.com)'
        instagram_pattern = r'(https?://)(www\.)?(instagram\.com)'
        replacements = {
            'twitter.com': 'fxtwitter.com',
            'x.com': 'fixupx.com',
            'reddit.com': 'rxddit.com',
            'tiktok.com': 'tfxktok.com',
            'vm.tiktok.com': 'tfxktok.com',
            'instagram.com': 'kkinstagram.com'
        }

        patterns = [twitter_pattern, reddit_pattern, tiktok_pattern, instagram_pattern]

        for pattern in patterns:
            match = re.search(pattern, message.content)
            if match:
                new_url = message.content
                for old, new in replacements.items():
                    new_url = re.sub(rf'https?://(www\.)?{old}', rf'https://{new}', new_url)
                await ctx.respond(new_url, ephemeral=True)
                return

        await ctx.respond("No supported link found!", ephemeral=True)


def setup(bot):
    bot.add_cog(MessageCommands(bot))
