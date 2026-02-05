import discord


class SlashCommands(discord.Cog, name="slash_commands"):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot


def setup(bot: discord.Bot) -> None:
    bot.add_cog(SlashCommands(bot))
