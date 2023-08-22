from os import environ

from disnake import Intents, Embed, ApplicationCommandInteraction
from disnake.ext import commands

bot = commands.Bot(
    command_prefix=".",
    intents=Intents.all(),
    test_guilds=[823820166478823462],
)

@bot.listen()
async def on_ready():
    print(f"Logged in {bot.user} ({bot.user.id})!")


Embed.set_default_color(0xf1c40f)  # старый глубокий синий - 283593

bot.load_extensions("cogs")
bot.load_extensions("events")

bot.run(environ.get('DISCORD_TOKEN'))
