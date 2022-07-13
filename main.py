# noinspection PyUnresolvedReferences
from random import choice

import disnake
from disnake.ext import commands

bot = commands.Bot(
    command_prefix=".",
    test_guilds=[823820166478823462],
    intents=disnake.Intents.all(),
    activity=disnake.Game("play.breadixpe.ru"),
    status=disnake.Status.idle,
    reload=True,  # Только для тестирования, не допускать в продакшн
)
disnake.Embed.set_default_color(283593)

logo_url = "https://media.discordapp.net/attachments/925973441524424716/925973455919251536/logo_bread.png"


@bot.event
async def on_ready():
    print("ГЛАВНАЯ * Загружена")


@bot.event
async def on_error(error: Exception, inter: disnake.ApplicationCommandInteraction):
    print(error)


@bot.event
async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error):
    """Обработчик ошибок"""
    if isinstance(error, commands.CommandError):
        texts = ["Извините!", "Простите!", "Ошибка"]
        error_embed = disnake.Embed(
            title=f":warning: | {choice(texts)}",
            description=f"Не удалось выполнить команду, код ошибки: {error}"
        )
        await inter.response.send_message(embed=error_embed, ephemeral=True)
    if isinstance(error, commands.CommandOnCooldown):
        texts = ["Повторите позже", "чуть позже!", "пару секунд!", "примите позу ожидания", "одну секундочку!", "щя",
                 "подождите"]
        error_embed = disnake.Embed(
            title=f":hourglass: | {choice(texts)}",
            description=f"Время перед повторным использованием: `{round(error.retry_after)}` сек."
        )
        await inter.response.send_message(embed=error_embed, ephemeral=True)
    if isinstance(error, commands.CheckFailure):
        texts = ["Извините!", "Простите!"]
        error_embed = disnake.Embed(
            title=f":hourglass: | {choice(texts)}",
            description=f"Не удалось выполнить команду, для этого необходима роль: {error}"
        )
        await inter.response.send_message(embed=error_embed, ephemeral=True)


# help command here

bot.load_extensions("cogs")
# bot.run("ODc1MDg0MzgzMjg2MDg3Njkx.YRQX1w.DtmzpbMWMUvOpwS7U8YBkLPZr4c") #ОСНОВА
bot.run("OTI0Njk0MTAyODUzOTY3OTE0.GTzIPQ.vI9MQycBohV3kHQyWR2y2CZ57EV00yxRRWDCQ0")
