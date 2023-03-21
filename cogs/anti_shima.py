from disnake import Embed
from disnake.ext import commands
from disnake.ext.commands import Context, Bot, Cog


class AntiShimaCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.command()
    async def anti(self, ctx: Context):
        await ctx.send(f".")
        while True:
            shima = await self.bot.fetch_user(440855229941022721)
            await shima.move_to(channel=None, reason="Шима очень плохо себя ведёт")


def setup(bot: Bot) -> None:
    bot.add_cog(AntiShimaCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
