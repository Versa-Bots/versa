import os

import discord
from dotenv import load_dotenv

bot = discord.Bot(intents=discord.Intents.default(),
                  default_command_integration_types=[discord.IntegrationType.user_install])

bot.load_extensions("src.cogs")
print("Loaded cogs: " + ', '.join(bot.cogs))


@bot.listen()
async def on_connect():
    print('Connected to Discord!')


@bot.listen()
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')

load_dotenv()
bot.run(os.getenv("TOKEN"))
