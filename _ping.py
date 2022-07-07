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

    @commands.command(name="пинг", aliases=["ping"])
    async def ping(self, ctx: commands.Context):
        """Получить задержку работы бота."""
        await ctx.send(f"Задержка: {round(self.bot.latency * 1000)}мл.")


def setup(bot):
    bot.add_cog(PingCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
