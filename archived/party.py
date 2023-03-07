import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction


# party
# id name channel_id creator = user_id (=disord_id)
#
# party_members
# party_id user_id (=disord_id)

async def send_to_party(party_id: int, embed: object):
    try:
        await thread.send()
    except HTTPException:
        channel = get()
        thread = channel.create_thread(name=f"Party: {name}")
        await thread.send()


class PartyCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="тусовка")
    async def party(self, inter: ApplicationCommandInteraction):
        pass

    @party.sub_command(name="создавть")  # TODO создавть, пригласит (добавить), узнать (инфо), позвать играть,
    async def create(self, inter: ApplicationCommandInteraction):
        """
        Найти людей для совместной игры
        Parameters
        ----------
        режим: Выберите сервер для игры
        """


def setup(bot: commands.Bot) -> None:
    bot.add_cog(PartyCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
