import aiosqlite
from aiosqlite import Error
from disnake import Embed, ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog

guild_id = 823820166478823462  # TEST
admin_channel_id = 1074308668364947538
log_channel_id = 1084879584715083786  # TEST
voice_create_channel_id = 997851742475669594

status_voice_channel_id = 1066055695914520606
status_text_channel_id = 1078357675622023228
status_message_id = 1084479038866866316

servers = ["SkyWars №1", "SkyWars №2", "BedWars №1", "BedWars №2", "BedWars №3", "Duels №1", "Murder Mystery №1",
           "Murder Mystery №2", "Survival №1"]

server_names = "SkyWars №1, SkyWars №2, BedWars №1, BedWars №2, BedWars №3, Duels №1, Murder Mystery №1,  Murder Mystery №2, Survival №1"
games_modes_names = "skywars, bedwars, duels, survival, murder_mystery"

data_storage = "general"  # genaral or test

async def get_connection() -> object:
    global data_storage
    try:
        connect = await aiosqlite.connect(f"{data_storage}.db")
        return connect

    except Error as e:
        print(f": {e}")



async def get_data_config(inter: ApplicationCommandInteraction, data_key: str):
    create_discord_users = """
    CREATE TABLE IF NOT EXISTS test_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        value TEXT UNIQUE
    );
    """
    try:
        connect = await get_connection()
        cursor = await connect.cursor()
        await cursor.execute(create_discord_users)

    except Error as e:
        await inter.response.send_message()

    finally:
        await connect.close()

async def update_data_config(name: str, value: str):
    ...

class Config(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="конфиг")
    @commands.is_owner()
    async def config(self, inter: ApplicationCommandInteraction):
        pass

    @config.sub_command(name="таблица")
    @commands.is_owner()
    async def change_config(
            self,
            inter: ApplicationCommandInteraction,
            new_data_storage: str = commands.Param(choices=["genaral", "test"])
    ):
        global data_storage
        data_storage = new_data_storage
        embed = Embed(
            title="Конфиг изменён",
            description=f"Новая таблица: {data_storage}"
        )

        await inter.send(embed=embed, ephemeral=True)

    @config.sub_command(name="список")
    @commands.is_owner()
    async def data_list_config(
            self,
            inter: ApplicationCommandInteraction,
            name: str,
            value: str
    ):
        await update_data_config(name, value)
        embed = Embed(
            title="Данные в конфиге обновлены",
            description=f"Новое значение для поля {name} : {data_storage}"
        )
        await inter.send(embed=embed, ephemeral=True)

    @config.sub_command(name="добавить")
    @commands.is_owner()
    async def add_to_config(
            self,
            inter: ApplicationCommandInteraction,
            name: str,
            value: str
    ):
        await update_data_config(name, value)

        embed = Embed(
            title="Добавлены данные в конфиг",
            description=f"Новое значение {name} : {data_storage}"
        )

        await inter.send(embed=embed, ephemeral=True)

    @config.sub_command(name="обновить")
    @commands.is_owner()
    async def update_config(
            self,
            inter: ApplicationCommandInteraction,
            name: str,
            value: str
    ):
        await update_data_config(name, value)

        embed = Embed(
            title="Обновлены данные в конфиге",
            description=f"Новое значение для поля {name } : {data_storage}"
        )

        await inter.send(embed=embed, ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(Config(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
