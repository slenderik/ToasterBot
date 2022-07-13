# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands
from main import logo_url


class PlayCog(commands.Cog):
    """Команда задержки бота."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="играть")
    async def play(self, inter: disnake.ApplicationCommandInteraction):
        """Поможет вам зайти на сервер!"""
        play_button = disnake.ui.View()
        play_button.add_item(disnake.ui.Button(
            label="Зайти поиграть на сервер",
            style=disnake.ButtonStyle.url,
            url="https://breadixpe.ru/play"
        ))
        play_embed = disnake.Embed(
            title="BreadixWorld",
            description="**адрес:** play.breadixpe.ru:19132"
                        ""
        )  # .set_thumbnail(url=logo_url)
        play_embed.set_author(name="BreadixWorld", icon_url=logo_url, url="https://breadixpe.ru/play")
        await inter.response.send_message(embed=play_embed, view=play_button, ephemeral=True)


def setup(bot):
    bot.add_cog(PlayCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
