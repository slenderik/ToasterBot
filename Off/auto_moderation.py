# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands


class AutoModCog(commands.Cog):
    """Автомодерация плохих сообщений"""

    #спам (повторяемые сообщения), злоупотребление пингами, пинг еврика
    #мат, оскорбления

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Отправить сообщение, выдать пред, удалить сообщениек."""
        #список мата
        profanity = ["блять", "бля", "ебать", "нахуй", "пизда", "пиздец", "ахуеть", "ахуел", "ебанутый", "ебануться"]

        
        msg = message.content.lower()
        msg.split()
        #msg = msg.strip()
        #msg = msg.replace(" ", ", ")
        #msg = msg.replace("...", ", ")
        #msg = msg.replace("..", ", ")
        #msg = msg.replace(".", ", ")
        #msg = msg.replace("-", ", ")
        #msg = msg.replace("–", ", ")
        #msg = msg.replace("—", ", ")

        text = msg.split(", ")
        for word in text:
            if word in profanity:
                await message.delete()
                member = message.author
                emb = disnake.Embed(
                    title="Текст сообщения:",
                    description=message.content,
                    colour=0xF93A2F
                )
                emb.add_field(
                    name="**Нарушение**: ```Мат в сообщение```",
                    value=f"**Запрещённое слово**: ||{word}||"
                )
                emb.set_footer(text="Зажмите на тексте, для копирования.")

                await member.send("<:bread_rage:879387116528861224> | Сообщение удалено.", embed=emb)

        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(AutoModCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")

