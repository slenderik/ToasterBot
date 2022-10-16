# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands


class AntiPingCog(commands.Cog):
    """О не пинговании меня или другого стафа"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     """"Автоответчик на пинги."""
    #
    #     stuff_ids = ["<@968313032755249232>", "<@369174650053459979>", "<@>", ]
    #     team_ids = ["<@324922480642752512>", "<@389137312300400654>"]
    #
    #     print(message.content)
    #     if message.content in stuff_ids and not message.author.bot:
    #         print("aaa")
    #         embed = disnake.Embed(
    #             title=f"Хей, {message.author.display_name}",
    #             description=f"Пожалйста не упоминайте администрацию. \nЕсли вам нужна помощь, упоминайте <@&928641653344972860>"
    #         )
    #         channel = message.channel
    #         await channel.send(embed=embed)
    #     elif message.content in team_ids and not message.author.bot:
    #         print("aaa")
    #         embed = disnake.Embed(
    #             title=f"Хей, {message.author.display_name}",
    #             description="""Не нужно пинговать администрацию.
    #                             Если вам нужна помощь, упоминайте <@&928641653344972860>
    #                         """
    #         )
    #         channel = message.channel
    #         await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(AntiPingCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
