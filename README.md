# versa
Versa is a Discord app (bot) aimed to provide helpful utility commands

# What is this?

Versa is a simple utility Discord bot, with the main goal of being open source and self-hosting friendly.

# Self-Hosting

1. Create an application on https://discord.com/developers/applications
2. Generate an OAuth link and add install the bot to your Discord account (this bot is intended as a user app)
3. Clone your repository onto a VPS or your own PC with `git clone <your repo url.git>`
4. Make sure Python 3.13+ is installed
5. Run `pip install -r requirements.txt` TODO Update to uv when we do it
6. Use PM2 or a similar tool to run the bot (`pm2 start bot.py --name Versa --interpreter python3`)

#### ⚠ **Further support with self-hosting will not be provided.** ⚠

# License

This project is licensed under AGPL-3.0. Forks and redistributions must remain open-source. See the LICENSE file for
further info