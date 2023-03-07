from aiohttp import ClientSession
from disnake import ApplicationCommandInteraction, Embed
from disnake.ext import commands

import datetime
from calendar import monthrange

class MoneyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")



    @commands.slash_command(name="деньги")
    async def money(self, inter: ApplicationCommandInteraction, time: int):

        async def request() -> object:
            """Вернуть информацию поиска по никнейму, в группе с донатами."""
            TOKEN = "25991c5d25991c5d25991c5d6d25e1ebfb2259925991c5d447917c5be90392810a81ccd"
            VERSION = "5.131"
            GROUP_NAME = "breadixdonations"
            OWNER_ID = "-151687251"
            COUNT = "100"
            async with ClientSession() as session:
                async with session.get(
                        f"https://api.vk.com/method/wall.get?"
                        f"access_token={TOKEN}"
                        f"&v={VERSION}"
                        f"&domain={GROUP_NAME}"
                        f"&owner_id={OWNER_ID}"
                        f"&owners_only=1"
                        f"&count={COUNT}") as r:
                    if r.status == 200:
                        js = await r.json()
                        return js

        def price(purchase: str, amount: int) -> int:
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
            return purchase_price.get(purchase) * amount

        running = True
        while running:
            response = await request()

            purchase_count = {
                "fly": 0,
                "vip+": 0,
                "vip": 0,
                "vip surv": 0,
                "mvp++": 0,
                "mvp+": 0,
                "mvp": 0,
                "creative+": 0,
                "creative": 0,
                "разбан": 0,
                "1000 монет": 0,
                "5000 монет": 0,
                "10000 монет": 0,
                "пожертвования": 0
            }
            servers_count = {
                "bedwars": {},
                "skywars": {},
                "murder mystery": {},
                "survival": {},
                "duels": {}
            }

            for i in range(100):
                time = response["response"]["items"][i]["date"]

                date = datetime.date(2021, 5, 16)
                d = date.replace(day=calendar.monthrange(date.year, date.month)[1])
                d.toordinal

                # if 1664571600 > time:
                #     continue
                # elif time < 1667163600:
                #     running = False
                #     break

                products = ("fly", "vip+", "vip", "mvp++", "mvp+", "mvp", "creative+", "creative", "разбан",
                            "1000 монет", "5000 монет", "10000 монет", "пожертвования")
                servers = ("bedwars", "skywars", "murder mystery", "murdermystery", "survival", "duels")

                text = response["response"]["items"][i]["text"].lower()
                purchase = None

                for product in products:
                    if int(text.find(product)) != -1:
                        if product == "vip" and int(text.find("surv")) != -1:
                            purchase = product + " surv"
                        else:
                            purchase = product

                for server in servers:
                    if int(text.find(server)) != -1:
                        if server == "murdermystery":
                            server = "murder mystery"

                        server = servers_count.get(server)  # add purchase to server list
                        if not server.get(purchase):
                            server[purchase] = 1
                        else:
                            server[purchase] += 1

                purchase_count[purchase] += 1  # add to list of purchase

            embeds = []
            all_money = 0

            text = ""
            for product, amount in purchase_count.items():  # add embed
                text += f"{amount} {product} — {price(product, amount)}₽\n"
            # embeds.append(Embed(title="Товары за период", description=text))

            embed = Embed(title="Заработок BreadixWorld", description=text)
            for server_name, server_info in servers_count.items():
                text = ""
                money = 0
                for info in server_info.items():
                    text += f"{info[1]} {info[0]} — {price(info[0], info[1])}₽\n"
                    money += price(info[0], info[1])
                # text += f"На {server_name} "
                all_money += money

                embed.add_field(name=f"{server_name} — {money}₽", value=text, inline=False)
            embed.set_footer(text=f"Всего: {all_money}₽")
            embeds.append(embed)

            await inter.response.send_message(embeds=embeds)


def setup(bot):
    bot.add_cog(MoneyCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" - {__name__}")
