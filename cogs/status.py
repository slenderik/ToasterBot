# noinspection PyUnresolvedReferences
import time
import disnake
import datetime
from disnake.ext import commands


class StatusCog(commands.Cog):
    """Команда статуса"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.command(aliases=["статус"])
    @disnake.ext.commands.has_role(977974127304515614)
    async def status(self, ctx: commands.Context, *, text):
        """Отправить сообщение о проблемах."""
        await ctx.send(f"[ <t:{round(time.mktime(datetime.datetime.now().timetuple()))}:R> ] {text}")


def setup(bot):
    bot.add_cog(StatusCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
