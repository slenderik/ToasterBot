import disnake
from disnake.ext import commands


class NewsThreadCog(commands.Cog):
    """Ветки для новостей"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Создать ветку для комментариев в канале новостей"""
        if message.channel.id == 610146698681122827:
            try:
                await message.channel.create_thread(name="Комментарии", message=message, slowmode_delay=10)
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(NewsThreadCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
