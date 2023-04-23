import aiosqlite
from aiosqlite import Error
from disnake import Embed, ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog

guild_id = 823820166478823462  # TEST
admin_channel_id = 1074308668364947538
audit_log_channel_id = 1084879584715083786  # TEST
voice_create_channel_id = 997851742475669594

status_voice_channel_id = 1066055695914520606
status_text_channel_id = 1078357675622023228
status_message_id = 1084479038866866316

servers = ["SkyWars №1", "SkyWars №2", "BedWars №1", "BedWars №2", "BedWars №3", "Duels №1", "Murder Mystery №1",
           "Murder Mystery №2", "Survival №1"]

SERVERS_PORTS = {
    'SkyWars': [4108, 5732],
    'BedWars': [6360, 4248, 1313],
    'Murder Mystery': [9624, 7198],
    'Survival': [59898],
    'Duels': [7219]
}

server_emojis = {
    4108: '<:sw1:1077962812996993064>',
    5732: '<:sw2:1077962839517573192>',
    6360: '<:bw1:1077962902289518673>',
    4248: '<:bw2:1077962930739499171>',
    1313: '<:bw3:1077962956601561171>',
    9624: '<:mm1:1077962982807584860>',
    7198: '<:mm2:1077963008107622492>',
    59898: '<:surv:1059520290461339778>',
    7219: '<:duels:1059520345775800391>',
}


async def get_connection() -> object:
    global data_storage
    try:
        connect = await aiosqlite.connect(f"{data_storage}.db")
        return connect

    except Error as e:
        print(f": {e}")


data_storage = "general"  # genaral or test

async def get_data_config(data_key: str):
    create_discord_users = """
    CREATE TABLE IF NOT EXISTS discord_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        NID INTEGER NOT NULL,
        discord_id INTEGER NOT NULL,
        FOREIGN KEY (NID) REFERENCES users(NID) ON DELETE CASCADE
        CONSTRAINT discord_id_uq UNIQUE(discord_id)
    );
    """
    try:
        connect = await get_connection()
        cursor = await connect.cursor()

    except Error as e:
        print(f"[ДОБАВИТЬ НИК АЙДИ ИЗ ДС АЙДИ] Ошибка: {e}")

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
