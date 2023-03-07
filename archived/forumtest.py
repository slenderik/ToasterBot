from disnake.ext import commands
from disnake import Embed


class ForumCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.command()
    async def post(self, ctx: commands.Context):
        """Получить задержку работы бота."""
        embed = Embed(colour=0xf1c40f)
        embed.add_field(
            name="Встречайте! Новые хелперы:",
            value="+ monyaRabb1t_ • Подобрана с улицы! :cat:\n"
                  "+ peremotka • Становится хелпером!\n"
                  "⠀",
            inline=False
        )
        embed.add_field(
            name="Покинули нас:",
            value="- GARFIELD • Не активность\n"
                  "- IValeska • Не активность\n"
                  "- Crostar • ПСЖ\n"
                  "⠀",
            inline=False
        )
        embed.add_field(
            name="Актуальный список помощников",
            value="1. nikto\_I\_vsyo\n"
                  "2. \_patron\_\n"
                  "3. DeBcTBeHHoCTb\n"
                  "4. Shima\_\n"
                  "5. \_sad\_Kodya\_\n"
                  "6. virgindronik\n"
                  "7. catlucif6226\n"
                  "8. kamuro\_san\n"
                  "9. devotion\n"
                  "10. peremotka\n"
                  "11. monyaRabb1t\_\n"
                  "⠀",
            inline=False
        )
        embed.set_footer(text="Прошу встретить новичков в комментариях!")
        forum = await ctx.guild.fetch_channel(1019989460311621652)
        await forum.create_thread(name="-", content="⠀", embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ForumCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
