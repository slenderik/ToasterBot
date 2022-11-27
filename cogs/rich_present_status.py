from random import choice

from disnake import Game
from disnake.ext import tasks, commands


class GameStatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.game_status.start()
        bot = await self.bot.change_presence(activity=Game("Проснулся"))

    @tasks.loop(minutes=10.0)
    async def game_status(self):
        print("anime")
        servers = ("SkyWars", "BedWars", "Duels", "Murder Mystery", "Survival")
        bot = await self.bot.change_presence(activity=Game(choice(servers)))


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GameStatusCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
