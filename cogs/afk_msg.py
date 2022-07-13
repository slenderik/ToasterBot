# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands


class AfkMsgCog(commands.Cog):
    """апрар"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """"Отправить сообщение о"""
        # Eсли участник зашёл/перешёл/вышел.
        # before.channel = None - зашел в гс сервера
        # after.channel = None - вышел с гс сервера

        afk_id = 948280920820047872

        if after.channel is not None and after.channel.id == afk_id:
            await after.channel.send("Эй, похоже вы немного отошли? Надеемся с вами всё хорошо ^^ Мы вас отключим от этого канала через пару минут.")


def setup(bot):
    bot.add_cog(AfkMsgCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")

