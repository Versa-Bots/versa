"""
error_handler.py

A simple error handling cog using on_application_command_error and on_command_error events.
This handles events for both application (slash) commands and text (prefixed) commands.

All code is correct as of, and has been tested with, Python 3.13.11 with py-cord v2.7.0 as required in pyproject.toml


Cog written by tobezdev:
    Github: https://github.com/tobezdev
    Website: https://tobezdev.com
"""

import discord
from discord import errors
from discord.ext import commands

import string, random


def get_msg_for_exception_type(error) -> str:
    msg: str | None = None
    errcode: str = "".join(
        random.choices(
            population=string.ascii_uppercase + string.ascii_lowercase + string.digits,
            k=12,
        )
    )

    match error:
        case commands.CommandNotFound():
            msg = "That command doesn't exist."
        case commands.MissingRequiredArgument():
            msg = "You forgot to include a required argument."
        case commands.BadArgument():
            msg = "One or more arguments were invalid or in the wrong format."
        case commands.DisabledCommand():
            msg = "That command is currently disabled."
        case commands.NoPrivateMessage():
            msg = "This command can't be used in DMs."
        case commands.MissingPermissions():
            msg = "You don't have the required permissions to use this command."
        case commands.BotMissingPermissions():
            msg = "I don't have the required permissions to perform that action."
        case commands.CommandOnCooldown():
            msg = "That command is on cooldown. Try again in a moment."
        case commands.MaxConcurrencyReached():
            msg = "Too many people are using this command at once. Please try again later."
        case errors.ExtensionFailed():
            msg = "An extension failed to load due to an internal error."
        case errors.ExtensionNotFound():
            msg = "Couldn't find that extension."
        case errors.ExtensionAlreadyLoaded():
            msg = "That extension is already loaded."
        case errors.ExtensionNotLoaded():
            msg = "That extension isn't currently loaded."
        case commands.NotOwner():
            msg = "Only the bot owner can use this command."
        case commands.CheckFailure():
            msg = "You didn't pass a permission or condition check for this command."
        case commands.CommandInvokeError():
            msg = "An unexpected error occurred while running that command."
        case discord.InteractionResponded():
            msg = "This interaction has already been responded to."
        case discord.ApplicationCommandInvokeError():
            msg = "Something went wrong while executing that application command."
        case discord.CheckFailure():
            msg = "You don't meet the requirements to run this interaction."
        case discord.Forbidden():
            msg = "I don't have permission to do that."
        case discord.NotFound():
            msg = "That resource couldn't be found."
        case discord.DiscordServerError():
            msg = "Discord's servers had an internal error."
        case discord.HTTPException():
            msg = "A request to Discord's API failed unexpectedly."
        case discord.ConnectionClosed():
            msg = "The connection to Discord was unexpectedly closed."
        case discord.GatewayNotFound():
            msg = "Couldn't connect to Discord's gateway."
        case discord.InvalidArgument():
            msg = "One or more arguments provided were invalid."
        case discord.InvalidData():
            msg = "Discord returned invalid or incomplete data."
        case discord.ClientException():
            msg = "The bot encountered a misuse or internal setup issue."
        case discord.LoginFailure():
            msg = "The bot token provided is invalid."

    if msg is None or not msg:
        msg = f"An unknown `{error.__class__.__name__}` error occurred while processing this command."

    msg += f"\nIf this error persists, please contact a member of staff. Quote error code **`{errcode}`** when reporting this issue."
    return msg


class ErrorHandler(discord.Cog, name="error_handler"):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    # Listner for application (slash) commands
    @discord.Cog.listener()
    async def on_application_command_error(
        self, interaction: discord.Interaction, exception: Exception
    ) -> None:
        #
        #
        print(exception)
        # This maintains the default implementation of printing to sys.stderr as specified on the docs here:
        # https://docs.pycord.dev/en/v2.7.0/api/clients.html#discord.Bot.on_application_command_error
        # This can be removed if the user does not want to print errors and only wants to handle them in Discord.

        error_message: str = get_msg_for_exception_type(exception)
        await interaction.respond(error_message, ephemeral=True)

    # Listener for text (prefix) commands
    @discord.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        #
        #
        print(error)
        # There is no default print for on_command_error, but I've added it here just to maintain the same
        # event style when the bot encounters an error.
        # https://docs.pycord.dev/en/v2.7.0/ext/commands/api.html#discord.discord.ext.commands.on_command_error
        # Like above, this can be removed if the user does not want to print errors.

        error_message: str = get_msg_for_exception_type(error)
        await ctx.message.reply(error_message)


def setup(bot: discord.Bot):
    bot.add_cog(ErrorHandler(bot))
