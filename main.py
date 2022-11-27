from os import environ

from disnake import Status, Intents, Embed
from disnake.ext import commands

bot = commands.Bot(
    command_prefix=".",
    test_guilds=[823820166478823462, 610142528271810560],
    intents=Intents.all(),
    status=Status.idle,
    reload=True  # Только для тестирования, не допускать в продакшн
)  # activity=disnake.Game("ip: play.breadixpe.ru \nport: 19132"),

Embed.set_default_color(0xf1c40f)  # старый голубокий синий - 283593

bot.load_extensions("cogs")
bot.load_extensions("events")

bot.run(environ.get('TOKEN'))
