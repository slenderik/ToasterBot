from random import choice
from re import split

from aiohttp import ClientSession
from disnake import UserCommandInteraction, MessageCommandInteraction, ApplicationCommandInteraction, ButtonStyle, User, \
    Message, Embed
from disnake.ext import commands
from disnake.ui import View, Button


async def get_purchases(nicknames: list[str]) -> Embed:
    async def request_to_donations(search_nickname: str) -> object:
        """Вернуть информацию поиска по никнейму, в группе с донатами."""
        TOKEN = "25991c5d25991c5d25991c5d6d25e1ebfb2259925991c5d447917c5be90392810a81ccd"
        VERSION = "5.131"
        GROUP_NAME = "breadixdonations"
        GROUP_ID = "-151687251"
        COUNT = "100"
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
            value = choice(("`Нет покупок :(`", "`Тут пустовато..`"))
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


class PurchasesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.user_command(name="Покупки")
    async def purchases_user_application(self, inter: UserCommandInteraction, user: User):
        embeds = await get_purchases([user.display_name, user.name])
        await inter.response.send_message(embeds=embeds, ephemeral=True)

    @commands.message_command(name="Покупки")
    async def purchases_message_application(self, inter: MessageCommandInteraction, message: Message):
        nicknames = split(" |, | ,|,", message.content)
        embeds = await get_purchases(nicknames)
        await inter.response.send_message(embeds=embeds, ephemeral=True)

    @commands.slash_command(name="покупки")
    async def purchases_slash_command(self, inter: ApplicationCommandInteraction, никнейм: str):
        """Посмотреть покупки

        Parameters
        ----------
        никнейм: Введите никнейм. Если несколько никнеймов - введите их через запятую
        """
        nickname = str(никнейм)
        nicknames = split(" |, | ,|,", nickname)

        embeds = await get_purchases(nicknames)

        buttons = View().add_item(
            Button(
                label="Купить донат можно здесь!", emoji="🛍️",
                style=ButtonStyle.url, url="https://shop.breadixpe.ru/"
            )
        )

        await inter.response.send_message(embeds=embeds, ephemeral=True, view=buttons)


def setup(bot):
    bot.add_cog(PurchasesCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" - {__name__}")
