from os import environ
from disnake import Embed
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot, Cog
from aiohttp import ClientSession


async def check_for_new_posts() -> bool:
    """Вернуть значение, появился ли новый пост."""
    TOKEN = environ.get('VK_TOKEN')
    VERSION = "5.131"
    GROUP_NAME = "club219396056"
    GROUP_ID = "-219396056"
    COUNT = "100"
    async with ClientSession() as session:
        async with session.get(
                f"https://api.vk.com/method/wall.get?"
                f"access_token={TOKEN}"
                f"&v={VERSION}"
                f"&domain={GROUP_NAME}"
                f"&owner_id={GROUP_ID}"
                f"&owners_only=1"  # новости (посты) только от сообщвества
                f"&count={COUNT}") as r:
            if r.status == 200:
                js = await r.json()
                return js


# response = await check_for_new_posts()
# post_count = response["response"]["count"]


async def create_embed_from_post(post_url: str) -> Embed:
    ...


class NewsCog(commands.Cog):
    def __init__(self, bot):
        self.post_count = 0
        self.bot = bot
        self.new_cheker.start()

    def cog_unload(self):
        self.new_cheker.cancel()

    @tasks.loop(seconds=14.0)
    async def new_cheker(self):
        resonse = await check_for_new_posts()
        # new_count = response["response"]["count"]
        # if post_count > post_count:
        #     ...

    @new_cheker.before_loop
    async def before_printer(self):
        print(f'[{__name__}] start')
        await self.bot.wait_until_ready()


def setup(bot: Bot) -> None:
    bot.add_cog(NewsCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
