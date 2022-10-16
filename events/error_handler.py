from random import choice

from disnake import ApplicationCommandInteraction, Embed
from disnake.ext import commands


class ErrorsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: ApplicationCommandInteraction, error):
        """Обработчик ошибок"""
        if isinstance(error, commands.CommandError):
            texts = ["Извините!", "Простите!", "Ошибка"]
            error_embed = Embed(
                title=f":warning: | {choice(texts)}",
                description=f"Не удалось выполнить команду, код ошибки: {error}"
            )
            await inter.response.send_message(embed=error_embed, ephemeral=True)
        elif isinstance(error, commands.CommandOnCooldown):
            texts = ["Повторите позже", "чуть позже!", "пару секунд!", "примите позу ожидания", "одну секундочку!",
                     "щя",
                     "подождите"]
            error_embed = Embed(
                title=f":hourglass: | {choice(texts)}",
                description=f"Время перед повторным использованием: `{round(error.retry_after)}` сек."
            )
            await inter.response.send_message(embed=error_embed, ephemeral=True)
        elif isinstance(error, commands.CheckFailure):
            texts = ["Извините!", "Простите!"]
            error_embed = Embed(
                title=f":hourglass: | {choice(texts)}",
                description=f"Не удалось выполнить команду, для этого необходима роль: {error}"
            )
            await inter.response.send_message(embed=error_embed, ephemeral=True)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ErrorsCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
