import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog


class PingCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command()
    async def ping(self, inter: ApplicationCommandInteraction):
        """Получить задержку работы бота."""
        await inter.response.send_message(f"Задержка: {round(self.bot.latency * 1000)}мл.")


def setup(bot: Bot) -> None:
    bot.add_cog(PingCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
