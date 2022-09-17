import disnake
from aiohttp import ClientSession
from re import split
from disnake import Embed
from disnake.ext import commands
from random import choice


class PurchasesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="покупки")
    async def purchases(self, inter: disnake.ApplicationCommandInteraction, никнейм: str):
        """Посмотреть покупки по никнейму

        Parameters
        ----------
        никнейм: Введите никнейм игрока, покупки которого хотите посмотреть
        """
        print(inter.application_id)
        nickname = str(никнейм)
        nicknames = split(" |, | ,|,", nickname)
        purchase_embed = Embed(title=":shopping_bags: Покупки")

        async def request_to_donations(search_nickname) -> object:
            """Вернуть информацию поиска по никнейму, в группе с донатами."""
            TOKEN = "25991c5d25991c5d25991c5d6d25e1ebfb2259925991c5d447917c5be90392810a81ccd"
            VERSION = "5.131"
            GROUP_NAME = "breadixdonations"
            GROUP_ID = "-151687251"
            COUNT = "100"
            async with ClientSession() as session:
                async with session.get(
                        f"https://api.vk.com/method/wall.search?access_token={TOKEN}"
                        f"&v={VERSION}"
                        f"&domain="
                        f"{GROUP_NAME}"
                        f"&owner_id={GROUP_ID}"
                        f"&query={search_nickname}"
                        f"&owners_only=1&count={COUNT}") as r:
                    if r.status == 200:
                        js = await r.json()
                        return js

        def get_server(text) -> str:
            """Вернуть сервер из текста"""
            servers = ("bedwars", "skywars", "murder mystery", "murdermystery", "survival")
            numbers = ("№1", "№2", "№3")
            server_output = {
                "bedwars": "BW",
                "skywars": "SW",
                "murder mystery": "MM",
                "murdermystery": "MM",
                "survival": "surv"
            }
            for server in servers:
                if int(text.find(server)) != -1:
                    for number in numbers:
                        if text.find(number) != -1:
                            server = f"{server_output[server]}{number[1:]}"
                            return server

        def get_purchase(text) -> str:
            """Вернуть покупку из текста"""
            purchases = (
                "fly", "vip+", "vip", "mvp++", "mvp+", "mvp", "creative+", "creative", "разбан", "1000 монет",
                "5000 монет", "10000 монет", "пожертвования")

            for purchase in purchases:
                if int(text.find(purchase.lower())) != -1:
                    return purchase

        def get_nickname(text) -> str:
            """Вернуть никнейм из текста"""
            text = text[6:]
            if int(text.find("купил")) != -1:
                return text[:int(text.find("купил")) - 1]
            elif int(text.find("приобрел")) != -1:
                return text[:int(text.find("купил")) - 1]

        def get_url(response: object, i: int) -> str:
            """Вернуть ссылку на пост ВКонтакте"""
            owner_id = str(response["response"]["items"][i]["owner_id"])
            url_id = str(response["response"]["items"][i]["id"])
            return "https://vk.com/wall" + owner_id + "_" + url_id

        def get_name(text) -> str:
            """"Вернуть изменённый никнейм"""
            return text.replace("_", "\\_")

        async def add_field(name):
            """Добавить строчку постов по никнейму."""
            post_text = ""
            response = await request_to_donations(name)
            post_count = response["response"]["count"]

            # добавляем текст всех покупок
            for i in range(post_count):
                text = response["response"]["items"][i]["text"].lower()
                post_text += f"`{i + 1}.` [{get_nickname(text)} | {get_server(text)} | {get_purchase(text)}]({get_url(response, i)})\n "

            # добавляем строку с никнеймом.
            if post_count == 0:
                title = get_name(name)
                none = ("`Нет покупок`", "`Пусто`", "`Нужно купить`")
                value = choice(none)
            else:
                title = f"{get_name(name)} ({post_count})"
                value = f"{post_text}"
            purchase_embed.add_field(name=title, value=value, inline=False)

        # Для каждого никнейма добавляем строчку с результатом поиска покупок
        for nickname in nicknames:
            await add_field(nickname)

        await inter.response.send_message(embed=purchase_embed, ephemeral=True)


def setup(bot):
    bot.add_cog(PurchasesCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" - {__name__}")
