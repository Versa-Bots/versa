"""Error handler cog.

A simple error handling cog using on_application_command_error and on_command_error events.
This handles events for both application (slash) commands and text (prefixed) commands.

All code is correct as of, and has been tested with, Python 3.13.11 with py-cord v2.7.0 as required in pyproject.toml


Cog written by tobezdev:
    Github: https://github.com/tobezdev
    Website: https://tobezdev.com
"""

import secrets
import string

import discord
from discord import errors
from discord.ext import commands

_ERROR_MESSAGES: tuple[tuple[type[BaseException], str], ...] = (
    (commands.CommandNotFound, "That command doesn't exist."),
    (commands.MissingRequiredArgument, "You forgot to include a required argument."),
    (commands.BadArgument, "One or more arguments were invalid or in the wrong format."),
    (commands.DisabledCommand, "That command is currently disabled."),
    (commands.NoPrivateMessage, "This command can't be used in DMs."),
    (commands.MissingPermissions, "You don't have the required permissions to use this command."),
    (commands.BotMissingPermissions, "I don't have the required permissions to perform that action."),
    (commands.CommandOnCooldown, "That command is on cooldown. Try again in a moment."),
    (commands.MaxConcurrencyReached, "Too many people are using this command at once. Please try again later."),
    (errors.ExtensionFailed, "An extension failed to load due to an internal error."),
    (errors.ExtensionNotFound, "Couldn't find that extension."),
    (errors.ExtensionAlreadyLoaded, "That extension is already loaded."),
    (errors.ExtensionNotLoaded, "That extension isn't currently loaded."),
    (commands.NotOwner, "Only the bot owner can use this command."),
    (commands.CheckFailure, "You didn't pass a permission or condition check for this command."),
    (commands.CommandInvokeError, "An unexpected error occurred while running that command."),
    (discord.InteractionResponded, "This interaction has already been responded to."),
    (
        discord.ApplicationCommandInvokeError,
        "Something went wrong while executing that application command.",
    ),
    (discord.CheckFailure, "You don't meet the requirements to run this interaction."),
    (discord.Forbidden, "I don't have permission to do that."),
    (discord.NotFound, "That resource couldn't be found."),
    (discord.DiscordServerError, "Discord's servers had an internal error."),
    (discord.HTTPException, "A request to Discord's API failed unexpectedly."),
    (discord.ConnectionClosed, "The connection to Discord was unexpectedly closed."),
    (discord.GatewayNotFound, "Couldn't connect to Discord's gateway."),
    (discord.InvalidArgument, "One or more arguments provided were invalid."),
    (discord.InvalidData, "Discord returned invalid or incomplete data."),
    (discord.ClientException, "The bot encountered a misuse or internal setup issue."),
    (discord.LoginFailure, "The bot token provided is invalid."),
)


def generate_error_code(length: int = 12) -> str:
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def get_error_message(error: Exception) -> str:
    msg: str | None = None
    errcode: str = generate_error_code()

    for exc_type, exc_msg in _ERROR_MESSAGES:
        if isinstance(error, exc_type):
            msg = exc_msg
            break

    if msg is None or not msg:
        msg = f"An unknown `{error.__class__.__name__}` error occurred while processing this command."

    msg += (
        "\nIf this error persists, please contact a member of staff. "
        f"Quote error code **`{errcode}`** when reporting this issue."
    )
    return msg


class ErrorHandler(discord.Cog, name="error_handler"):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    # Listener for application (slash) commands
    @discord.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, exception: Exception) -> None:
        print(exception)
        # This maintains the default implementation of printing to sys.stderr as specified on the docs here:
        # https://docs.pycord.dev/en/v2.7.0/api/clients.html#discord.Bot.on_application_command_error
        # This can be removed if the user does not want to print errors and only wants to handle them in Discord.

        error_message: str = get_error_message(exception)
        await interaction.respond(error_message, ephemeral=True)


def setup(bot: discord.Bot) -> None:
    bot.add_cog(ErrorHandler(bot))
