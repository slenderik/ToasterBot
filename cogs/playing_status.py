from random import choice

from disnake import Game
from disnake.ext import tasks, commands
from utils.config import servers


class GameStatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.playing_status.start()

    @tasks.loop(minutes=10.0)
    async def playing_status(self):
        await self.bot.change_presence(activity=Game(choice(servers)))

    @playing_status.before_loop
    async def before_playing_status(self):
        print('[Игровой статус] Начинаем')
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GameStatusCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
