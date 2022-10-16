from os import environ

import disnake
from disnake.ext import commands

bot = commands.Bot(
    command_prefix=".",
    test_guilds=[823820166478823462],
    intents=disnake.Intents.all(),
    activity=disnake.Game("ip: play.breadixpe.ru \nport: 19132"),
    status=disnake.Status.idle,
    reload=True,  # Только для тестирования, не допускать в продакшн
)

disnake.Embed.set_default_color(283593)

logo_url = "https://media.discordapp.net/attachments/925973441524424716/925973455919251536/logo_bread.png"

bot.load_extensions("cogs")
bot.load_extensions("events")

bot.run(environ.get('BETATOKEN'))
