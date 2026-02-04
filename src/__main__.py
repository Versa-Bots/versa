import os

import discord
from dotenv import load_dotenv

bot = discord.Bot(intents=discord.Intents.default())

bot.load_extensions("src.cogs")
print("Loaded cogs: " + ", ".join(bot.cogs))


@bot.listen()
async def on_connect() -> None:
    print("Connected to Discord!")


@bot.listen()
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    print("------")


load_dotenv()
bot.run(os.getenv("TOKEN"))
