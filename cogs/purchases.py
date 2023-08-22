from os import environ
from re import split

from numpy import arange
from aiohttp import ClientSession
from disnake import Embed, UserCommandInteraction, ApplicationCommandInteraction, MessageCommandInteraction, \
    ButtonStyle, Message, User
from disnake.ext import commands
from disnake.ui import View, Button


async def request(nickname: str) -> object:
    """Вернуть информацию поиска по никнейму, в группе с донатами."""
    TOKEN = environ.get('VK_TOKEN')
    VERSION = "5.131"
    GROUP_NAME = "breadixdonations"
    GROUP_ID = "-151687251"  # id группы с донатами
    COUNT = "100"  # Максимум 100 постов за один запрос.
    async with ClientSession() as session:
        async with session.get(
                f"https://api.vk.com/method/wall.search?"
                f"access_token={TOKEN}"
                f"&v={VERSION}"
                f"&domain={GROUP_NAME}"
                f"&owner_id={GROUP_ID}"
                f"&query={nickname}"
                f"&owners_only=1"
                f"&count={COUNT}"
        ) as request:
            if request.status == 200:
                js = await request.json()
                return js


async def create_purchase_embed(nicknames: list[str]) -> list[Embed]:
    def server_name(text: str) -> str:
        numbers = ("№0, №1", "№2", "№3")
        servers = {
            "bedwars": "BW",
            "skywars": "SW",
            "murder mystery": "MM",
            "murdermystery": "MM",
            "survival": "SU",
            "duels": "DU"
        }

        # Получаем совпадения из текста и списка.
        name = set(servers.keys()) & set(text.lower().split())
        number = set(numbers) & set(text.lower().split())

        return servers["".join(name)] + "".join(number)[1:]

    def url(response: object, i: int) -> str:
        """Вернуть ссылку на пост ВКонтакте"""
        owner_id = str(response["response"]["items"][i]["owner_id"])
        url_id = str(response["response"]["items"][i]["id"])
        return "https://vk.com/wall" + owner_id + "_" + url_id

    price_purchase = {
        "vip+": 369,
        "vip": 79,
        "vip survival": 229,
        "mvp+": 319,
        "mvp++": 619,
        "mvp": 159,
        "fly": 39,
        "creative+": 619,
        "creative": 129,
        "разбан": 240,
        "1000 монет": 49,
        "5000 монет": 159,
        "10000 монет": 249,
        "пожертвования": 29
    }

    def price(text: str) -> int:
        text = text.lower().split()

        # если покупка на сюрва
        if "Survival" in text and "vip" in text:
            return price_purchase["vip survival"]

        # получаем покупку из текста
        purchase = set(price_purchase.keys()) & set(text)
        return price_purchase["".join(purchase)]

    embeds = []

    # Для каждого никнейма создаём ембед с покупоками
    for nickname in nicknames:
        response = await request(nickname)
        post_count = response["response"]["count"]

        if post_count == 0:
            embed = Embed(
                title=f":shopping_bags: {nickname}",
                description="Нет покупок."
            )
            embeds.append(embed)
            continue

        full_cost = 0
        post_text = ""

        # Состовляем текст всех покупок
        for post_number in arange(post_count):
            text = response["response"]["items"][post_number]["text"].lower()

            # TODO никнеймы
            # nickname_in_post = nickname(text)
            # if nickname != nickname_in_post:
            #     continue

            words = [
                "игрок ", "приобрел ", "купил ", "на ", "привилегию ", "купить донат — shop.breadixpe.ru", "!", "на "
                                                                                                                "——————————————————",
                "донат можно приобрести shop.breadixpe.ru", "——————————————————",
                f"{nickname} "]

            for i in words:
                text = text.replace(i, "")
            text = text.rstrip()

            post_text += f"`{post_number + 1}.` [{server_name(text)}]({url(response, post_number)}) \n"
            full_cost += price(text)

        embed = Embed(
            title=f":shopping_bags: {nickname} ({post_count})",
            description=f"{post_text}"
        )
        embed.set_footer(text=f"От {round(full_cost / 2)} до {full_cost} ₽")
        embeds.append(embed)


async def get_available_privileges(nickname: str) -> list[str] | None:
    all_privileges = ("fly", "vip", "vip+", "mvp", "mvp+", "mvp++", "creative", "creative+")

    response = await request(nickname)
    buy_count = response["response"]["count"]

    if buy_count == 0:
        return None

    privileges = {}

    for buy in arange(buy_count):
        text = response["response"]["items"][buy]["text"].lower()

        privilege = None
        for i in all_privileges:
            if i in text:
                privilege = i
                break

        if privilege is None:
            continue

        server_name = server_name(text)

        if server_name in privileges:
            # check best privilege
            previous_privilege = privileges.get(server_name)
            if all_privileges.index(privilege) > all_privileges.index(previous_privilege):
                privileges.update(server_name=privilege)

        if privilege not in privileges:
            privileges.update(server_name=privilege)

    return privileges.values()


class PurchasesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="покупки")
    async def purchases_slash_command(self, inter: ApplicationCommandInteraction, nickname: str):
        """Посмотреть покупки по никнейму

        Parameters
        ----------
        nickname: Введите никнейм игрока, покупки которого хотите посмотреть
        """
        store_button = View()
        button = Button(emoji="🛍️", label="Сайт авто-доната", style=ButtonStyle.url, url="https://shop.breadixpe.ru/")
        store_button.add_item(button)
        embeds = await create_purchase_embed(nicknames=split(" |, | ,|,", nickname))
        await inter.response.send_message(embeds=embeds, ephemeral=True, view=store_button)

    @commands.slash_command(name="покупки2")
    async def purchases_slash_command2(self, inter: ApplicationCommandInteraction, nickname: str):
        """Посмотреть покупки по никнейму

        Parameters
        ----------
        nickname: Введите никнейм игрока, покупки которого хотите посмотреть
        """
        prvileges = await get_available_privileges(nickname)
        await inter.response.send_message(str(prvileges), ephemeral=True)

    @commands.message_command(name="Покупки")
    async def purchases_message_command(self, inter: MessageCommandInteraction, message: Message):
        embeds = await create_purchase_embed(nicknames=[message.author.display_name, message.author.name])
        await inter.response.send_message(embeds=embeds, ephemeral=True)

    @commands.user_command(name="Покупки")
    async def purchases_user_command(self, inter: UserCommandInteraction, user: User):
        embeds = await create_purchase_embed(nicknames=[user.display_name, user.name])
        await inter.response.send_message(embeds=embeds, ephemeral=True)


def setup(bot):
    bot.add_cog(PurchasesCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" - {__name__}")
