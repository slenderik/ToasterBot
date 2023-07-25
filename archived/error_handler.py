from random import choice

from disnake import ApplicationCommandInteraction, Embed
from disnake.ext import commands
from utils.config import admin_channel_id


class ErrorsCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        """Обработчик ошибок. Отправка админам."""
        try:
            channel = self.bot.fetch_channel(admin_channel_id)
            embed = Embed(title=f"Ошибка в {event}")
            embed.add_field(name=args, value=kwargs)
            await channel.send("[@ERROR] <@324922480642752512>", embed=embed)

        except Exception as e:
            print(f"{__name__} Error: {e}")

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: ApplicationCommandInteraction, error):
        """Обработчик ошибок"""
        if isinstance(error, commands.CommandOnCooldown):
            texts = ["Повторите позже", "чуть позже!", "пару секунд!", "примите позу ожидания", "одну секундочку!",
                     "подождите"]
            error_embed = Embed(
                title=f":hourglass:     {choice(texts)}",
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

        elif isinstance(error, commands.CommandError):
            texts = ["Извините!", "Простите!", "Ошибка"]
            error_embed = Embed(
                title=f":warning: | {choice(texts)}",
                description=f"Не удалось выполнить команду, код ошибки: {error}"
            )
            await inter.response.send_message(embed=error_embed, ephemeral=True)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ErrorsCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
