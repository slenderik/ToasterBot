# Создать ветку
import disnake
from disnake.ext import commands

class Text(commands.Cog):
    """Всё что связано с текстовыми каналами!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Всё что связано с текст. каналами!
        Создать ветку, добавить реакции
        """

        # Создать ветку для комментариев в канале новостей и объявлений.
        if message.channel.id in (610146698681122827, 930121833561329675, 823826045568286741, 825291849757491201):
            try:
                await message.channel.create_thread(name="Комментарии", message=message, slowmode_delay=10)
            except Exception as e:
                print(e)

        #
        if message.channel.id in (998418781586079776, 979088081909080064):
            try:
                like = self.bot.get_emoji(983973450467147838)
                dislike = self.bot.get_emoji(975689765338902569)
                await message.add_reaction(like)
                await message.add_reaction(dislike)
            except Exception as e:
                print(e)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Text(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
