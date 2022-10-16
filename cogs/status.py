from datetime import datetime
from disnake.ext import commands


class StatusCog(commands.Cog):
    """Команда статуса"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.command(aliases=["статус"])
    async def status(self, ctx: commands.Context, *, text):
        """Отправить сообщение о проблемах."""
        await ctx.message.delete()
        allow_users = [377383169420427264, 324922480642752512]
        if ctx.author.id in allow_users:
            await ctx.send(f"[ <t:{round(datetime.now().timestamp())}:R> ] {text}")


def setup(bot):
    bot.add_cog(StatusCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
