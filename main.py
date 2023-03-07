from os import environ

from disnake import Intents, Embed
from disnake.ext import commands

bot = commands.Bot(
    command_prefix=".",
    test_guilds=[823820166478823462],
    intents=Intents.all()
)

Embed.set_default_color(0xf1c40f)  # старый голубокий синий - 283593

bot.load_extensions("cogs")
bot.load_extensions("events")

bot.run(environ.get('TOKEN'))
