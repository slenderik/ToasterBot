from disnake import *
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog


class REMCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    # @commands.slash_command()
    # async def rem(self, ctx: commands.Context):
    #     """Получить задержку работы бота."""
    #     async for member in ctx.guild.members():
    #         if member.nickname.startswith(["!"]):
    #             await member.edit(nick=member.nickname)


def setup(bot: Bot) -> None:
    bot.add_cog(REMCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
