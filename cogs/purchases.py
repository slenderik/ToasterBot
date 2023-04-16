from os import environ
from re import split

from aiohttp import ClientSession
from disnake import Embed, UserCommandInteraction, ApplicationCommandInteraction, MessageCommandInteraction, \
    ButtonStyle, Message, User
from disnake.ext import commands
from disnake.ui import View, Button


async def create_purchase_embed(nicknames: list[str]) -> list[Embed]:
    """Вернуть ембеды покупок по никнеймам"""

    async def request_to_vk_donations(nickname: str) -> object:
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

    def get_server_name(text: str) -> str:
        """Вернуть название сервер из текста"""
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
        server_name = set(servers.keys()) & set(text.lower().split())
        number = set(numbers) & set(text.lower().split())

        print(servers["".join(server_name)] + "".join(number)[1:])

        return servers["".join(server_name)] + "".join(number)[1:]
    def get_url(response: object, i: int) -> str:
        """Вернуть ссылку на пост ВКонтакте"""
        owner_id = str(response["response"]["items"][i]["owner_id"])
        url_id = str(response["response"]["items"][i]["id"])
        return "https://vk.com/wall" + owner_id + "_" + url_id

    def get_price_purchase(text: str) -> int:
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
        purchases = (
            "fly", "vip+", "vip", "mvp++", "mvp+", "mvp", "creative+", "creative", "разбан", "1000 монет",
            "5000 монет", "10000 монет", "пожертвования")

        # получаем покупку из текста, создавая список из текста и сверяя списки.
        purchase = set(purchases) & set(text.lower().split())

        if set("Survival") & set(text.lower().split()):
            # Если покупка на сюрва
            return price_purchase["".join(purchase) + " survival"]
        else:
            # Если покупка не на сюрва
            return price_purchase["".join(purchase)]

    purchases_embeds = []

    # Для каждого никнейма создаём ембед с покупоками
    for nickname in nicknames:
        response = await request_to_vk_donations(nickname)
        post_count = response["response"]["count"]
        full_cost = 0
        post_text = ""

        # Состовляем текст всех покупок
        for post_number in range(post_count):
            text = response["response"]["items"][post_number]["text"].lower()

            words = [
                "игрок ", "приобрел ", "купил ","на ", "привилегию ", "купить донат — shop.breadixpe.ru", "!", "на "
                "——————————————————", "донат можно приобрести shop.breadixpe.ru", "——————————————————",
                f"{nickname} "]
            servers = {
                "bedwars": "BW",
                "skywars": "SW",
                "murder mystery": "MM",
                "murdermystery": "MM",
                "survival": "SU",
                "duels": "DU"
            }

            for i in words:
                text = text.replace(i, "")
            text = text.rstrip()

            server_name = "".join(set(servers.keys()) & set(text.split()))
            text = text.replace(server_name, servers[server_name])

            post_text += f"`{post_number + 1}.` [{text}]({get_url(response, post_number)}) \n"
            full_cost += get_price_purchase(text)

        if post_count == 0:
            title = f":shopping_bags: {nickname}"
            value = "Нет покупок."
        else:
            title = f":shopping_bags: {nickname} ({post_count})"
            value = f"{post_text}"

        # Создаём ембед
        embed = Embed(title=title, description=value)
        embed.set_footer(text=f"От {round(full_cost / 2)} до {full_cost} ₽")

        # Добавляем к ембедам
        purchases_embeds.append(embed)

    return purchases_embeds


class PurchasesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")
        await create_purchase_embed(nicknames=["double_master"])

    @commands.slash_command(name="покупки")
    async def purchases_slash_command(self, inter: ApplicationCommandInteraction, никнейм: str):
        """Посмотреть покупки по никнейму

        Parameters
        ----------
        никнейм: Введите никнейм игрока, покупки которого хотите посмотреть
        """
        store_button = View().add_item(Button(
            emoji="🛍️",
            label="Сайт авто-доната",
            style=ButtonStyle.url,
            url="https://shop.breadixpe.ru/"
        ))
        embeds = await create_purchase_embed(nicknames=split(" |, | ,|,", никнейм))
        await inter.response.send_message(embeds=embeds, ephemeral=True, view=store_button)

    @commands.message_command(name="Посмотреть покупки")
    async def purchases_message_command(self, inter: MessageCommandInteraction, message: Message):
        embeds = await create_purchase_embed(nicknames=[message.author.display_name, message.author.name])
        await inter.response.send_message(embeds=embeds, ephemeral=True)

    @commands.user_command(name="Узнать покупки")
    async def purchases_user_command(self, inter: UserCommandInteraction, user: User):
        embeds = await create_purchase_embed(nicknames=[user.display_name, user.name])
        await inter.response.send_message(embeds=embeds, ephemeral=True)


def setup(bot):
    bot.add_cog(PurchasesCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" - {__name__}")
