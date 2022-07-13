# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands


class PingCog(commands.Cog):
    """Команда задержки бота."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command()
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        """Получить задержку работы бота."""
        await inter.response.send_message(f"Задержка: {round(self.bot.latency * 1000)}мл.")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(PingCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
