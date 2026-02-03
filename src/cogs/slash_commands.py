import discord


class SlashCommands(discord.Cog, name="slash_commands"):
    def __init__(self, bot: discord.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(SlashCommands(bot))
