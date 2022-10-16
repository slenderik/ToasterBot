# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands


class PlayCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    plase = commands.option_enum(["Для себя", "Отправить в чат"])

    @commands.slash_command(name="играть")
    async def play(self, inter: disnake.ApplicationCommandInteraction, отправить: plase = None):
        """
        Поможет зайти на сервер!

        Parameters
        ----------
        отправить: Выберите, куда отправить кнопку!
        """
        play_embed = disnake.Embed(
            title="Так же для входа",
            description="Версия: MCPE 1.1.X ([1.1.5](https://www.google.ru/search?q=minecraft+PE+1.1.5))\n"
                        "IP: play.breadixpe.ru \n"
                        "Порт: 19132 (стандартный)"
        )
        play_button = disnake.ui.View().add_item(
            disnake.ui.Button(
                label="Зайти на сервер",
                style=disnake.ButtonStyle.url,
                url="https://breadixpe.ru/play"
            )
        )
        if отправить:
            await inter.response.send_message(embed=play_embed, view=play_button, ephemeral=True)
        else:
            await inter.channel.send(embed=play_embed, view=play_button)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(PlayCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
