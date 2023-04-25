from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog


async def anime():
    purchases = {
        "vip+": 369,
        "vip": 79,
        "vip survival": 229,
        "mvp+": 319,
        "mvp++": 619,
        "mvp": 159,
        "fly": 39,
        "creative+": 619,
        "creative": 129,
        "разбан": 240,
        "1000 монет": 49,
        "5000 монет": 159,
        "10000 монет": 249,
        "пожертвования": 29
    }


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
