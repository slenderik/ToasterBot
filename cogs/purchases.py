from os import environ
from random import choice
from re import split

import disnake
from aiohttp import ClientSession
from disnake import Embed, UserCommandInteraction, ApplicationCommandInteraction, MessageCommandInteraction
from disnake.ext import commands


class PurchasesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    async def get_purchases(self, inter: ApplicationCommandInteraction, nicknames: str) -> Embed:
        """Посмотреть покупки по никнейму

        Parameters
        ----------
        никнейм: Введите никнейм игрока, покупки которого хотите посмотреть
        """
        nicknames = split(" |, | ,|,", str(nicknames))

        async def request_to_donations(search_nickname: str) -> object:
            """Вернуть информацию поиска по никнейму, в группе с донатами."""
            TOKEN = environ.get('VK_TOKEN')
            VERSION = "5.131"
            GROUP_NAME = "breadixdonations"
            GROUP_ID=  "-151687251"  # id группы с донатами
            COUNT = "100"  # Всего 100 постов. Ожидается что больше 100 донатов на нике не будет.
            async with ClientSession() as session:
                async with session.get(
                        f"https://api.vk.com/method/wall.search?"
                        f"access_token={TOKEN}"
                        f"&v={VERSION}"
                        f"&domain={GROUP_NAME}"
                        f"&owner_id={GROUP_ID}"
                        f"&query={search_nickname}"
                        f"&owners_only=1"
                        f"&count={COUNT}") as r:
                    if r.status == 200:
                        js = await r.json()
                        return js

        def get_server(text: str) -> str:
            """Вернуть сервер из текста"""
            servers = ("bedwars", "skywars", "murder mystery", "murdermystery", "survival", "duels")
            numbers = ("№1", "№2", "№3")
            server_output = {
                "bedwars": "BW",
                "skywars": "SW",
                "murder mystery": "MM",
                "murdermystery": "MM",
                "survival": "surv",
                "duels": "duels"
            }
            for server in servers:
                if int(text.find(server)) != -1:
                    for number in numbers:
                        if text.find(number) != -1:
                            server = f"{server_output[server]}{number[1:]}"
                            return server

        def get_purchase(text: str) -> str:
            """Вернуть покупку из текста"""
            purchases = (
                "fly", "vip+", "vip", "mvp++", "mvp+", "mvp", "creative+", "creative", "разбан", "1000 монет",
                "5000 монет", "10000 монет", "пожертвования")

            for purchase in purchases:
                if int(text.find(purchase.lower())) != -1:
                    return purchase

        def get_nickname(text: str) -> str:
            """Вернуть никнейм из текста"""
            text = text[6:]

            if int(text.find("купил")) != -1:
                return text[:int(text.find("купил")) - 1].replace("_", "\_")

            if int(text.find("приобрел")) != -1:
                return text[:int(text.find("приобрел")) - 1].replace("_", "\_")

        def get_url(response: object, i: int) -> str:
            """Вернуть ссылку на пост ВКонтакте"""
            owner_id = str(response["response"]["items"][i]["owner_id"])
            url_id = str(response["response"]["items"][i]["id"])
            return "https://vk.com/wall" + owner_id + "_" + url_id

        def get_name(text: str) -> str:
            """"Вернуть изменённый никнейм"""
            return text.replace("_", "\_")

        def get_price(text: str) -> int:
            purchase_price = {
                "vip+": 369,
                "vip": 79,
                "vip surv": 229,
                "mvp+": 319,
                "mvp++": 619,
                "mvp": 159,
                "fly": 39,
                "creative+": 129,
                "creative": 619,
                "разбан": 240,
                "1000 монет": 49,
                "5000 монет": 159,
                "10000 монет": 249,
                "пожертвования": 29
            }
            purchases = (
                "fly", "vip+", "vip", "mvp++", "mvp+", "mvp", "creative+", "creative", "разбан", "1000 монет",
                "5000 монет", "10000 монет", "пожертвования")
            servers = ("BW", "SW", "MM", "MM", "surv", "duels")

            for purchase in purchases:
                if int(text.find(purchase.lower())) != -1:
                    if purchase != "vip":
                        return purchase_price[purchase]
                    else:
                        if int(text.find("Survival")) != -1:
                            return purchase_price[purchase]
                        else:
                            return purchase_price[f"{purchase} surv"]

        embeds = []

        async def add_embed(name: str):
            """Добавить строчку постов по никнейму."""
            response = await request_to_donations(name)
            post_count = response["response"]["count"]

            # Состовляем текст всех покупок
            price = 0
            post_text = ""
            for i in range(post_count):
                text = response["response"]["items"][i]["text"].lower()
                a = f"`{i + 1}.` [{get_nickname(text)} | {get_server(text)} | " \
                    f"{get_purchase(text)}]({get_url(response, i)})\n "
                post_text += a
                price += get_price(a)

            # Состовляем текст.
            if post_count == 0:
                title = f":shopping_bags: {get_name(name)}"
                value = choice(("`Нет покупок :(`", "`Тут пустовато..`", "`Можно было бы и купить!`"))
            else:
                title = f":shopping_bags: {get_name(name)} ({post_count})"
                value = f"{post_text}"

            embed = Embed(
                title=title, description=value
            ).set_footer(
                text=f"💸 {round(price - price * 0.2)} - {price} ₽"
            )

            embeds.append(embed)

        # Для каждого никнейма добавляем строчку с результатом поиска покупок
        for nickname in nicknames:
            await add_embed(nickname)

        return embeds

    @commands.slash_command(name="покупки")
    async def purchases(self, inter: ApplicationCommandInteraction, никнейм: str):
        """Посмотреть покупки по никнейму

        Parameters
        ----------
        никнейм: Введите никнейм игрока, покупки которого хотите посмотреть
        """
        store_button = disnake.ui.View().add_item(
            disnake.ui.Button(
                emoji="🛍️",
                label="Купить донат можно здесь!",
                style=disnake.ButtonStyle.url,
                url="https://shop.breadixpe.ru/"
            )
        )
        embeds = await self.get_purchases(inter=inter, nicknames=никнейм)
        await inter.response.send_message(embeds=embeds, ephemeral=True, view=store_button)

    @commands.user_command(name="Посмотреть покупки")
    async def avatar(self, inter: UserCommandInteraction, user: disnake.User):
        store_button = disnake.ui.View().add_item(
            disnake.ui.Button(
                emoji="🛍️",
                label="Купить донат можно здесь!",
                style=disnake.ButtonStyle.url,
                url="https://shop.breadixpe.ru/"
            )
        )
        embeds = await self.get_purchases(inter=inter, nicknames=f"{user.display_name}, {user.name}")
        await inter.response.send_message(embeds=embeds, ephemeral=True, view=store_button)

    @commands.message_command(name="Узнать покупки")
    async def reverse(self, inter: MessageCommandInteraction, message: disnake.Message):
        store_button = disnake.ui.View().add_item(
            disnake.ui.Button(
                emoji="🛍️",
                label="Купить донат можно здесь!",
                style=disnake.ButtonStyle.url,
                url="https://shop.breadixpe.ru/"
            )
        )
        embeds = await self.get_purchases(inter=inter,
                                          nicknames=f"{message.author.display_name}, {message.author.name}")
        await inter.response.send_message(embeds=embeds, ephemeral=True, view=store_button)


def setup(bot):
    bot.add_cog(PurchasesCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" - {__name__}")
