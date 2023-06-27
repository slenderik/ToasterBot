import aiosqlite
from aiosqlite import Error
from disnake.ext import commands
from utils.checks import discord_admins
from disnake.ext.commands import Bot, Cog
from disnake import ApplicationCommandInteraction


async def get_many():
    try:
        async with aiosqlite.connect("config.db", check_same_thread=False) as db:
            async with db.execute("SELECT role_id FROM roles") as cursor:
                row = await cursor.fetchall()
                return row

    except aiosqlite.Error as e:
        print(f"[ERROR {__name__}] {e}")


async def get_one(thing: str, role_id: str):
    async with aiosqlite.connect("confg.db", check_same_thread=False) as db:
        async with db.execute(f"SELECT {thing} FROM roles WHERE role_id = {role_id}") as cursor:
            row = await cursor.fetchone()
            return row[0]


guild_id = 823820166478823462  # TEST
admin_channel_id = 1074308668364947538
log_channel_id = 1084879584715083786  # TEST

status_voice_channel_id = 1066055695914520606
status_text_channel_id = 1078357675622023228
status_message_id = 1084479038866866316

servers = ["SkyWars №1", "SkyWars №2", "BedWars №1", "BedWars №2", "BedWars №3", "Duels №1", "Murder Mystery №1",
           "Murder Mystery №2", "Survival №1", "S.T.A.L.K.E.R."]

server_names = "SkyWars №1, SkyWars №2, BedWars №1, BedWars №2, BedWars №3, Duels №1, Murder Mystery №1,  " \
               "Murder Mystery №2, Survival №1, S.T.A.L.K.E.R."

games_modes_names = "skywars, bedwars, duels, survival, murder_mystery"

async def update(name: str, value: str):
    ...


# create_discord_users = """
#     CREATE TABLE IF NOT EXISTS test_config (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT UNIQUE,
#         value TEXT UNIQUE
#     );
#     """
#
#     request_get = f"SELECT data FROM {data_storage} WHERE key = {key}"
#     connect = await get_connection()
#     cursor = await connect.cursor(request_get)
#     data = await cursor.execute(create_discord_users)
#
#     await connect.close()
#     return data


class Config(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_connection(self) -> object:
        global data_storage
        try:
            connect = await aiosqlite.connect(f"config.db", check_same_thread=False)
            return connect

        except Error as e:
            print(f": {e}")

    async def get(self, key: str) -> str:
        request_get = f"SELECT data FROM {data_storage} WHERE key = {key}"
        connect = await self.get_connection()
        cursor = await connect.cursor()
        data = await cursor.execute(request_get)

        await connect.close()
        return data

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="конфиг")
    @commands.check(discord_admins)
    async def config(self, inter: ApplicationCommandInteraction):
        pass

    @config.sub_command(name="удалить")
    @commands.check(discord_admins)
    async def list(self, inter: ApplicationCommandInteraction, id: int):
        text = "Не удалось"
        async with aiosqlite.connect("MentionRolesThread.db", check_same_thread=False) as db:
            async with db.execute(f"SELECT * FROM roles WHERE id = {id}") as cursor:
                info = await cursor.fetchone()
                info = info[0]

                await db.execute(f"DELETE FROM roles WHERE id = {id}")
                await db.commit()
                text = f"{text[0]}. <@&{text[1]}> -> <#{text[2]}> \n" \
                       f"╰ {text[3]} \n"

        await inter.send(text, ephemeral=True)

    @config.sub_command(name="добавить")
    @commands.check(discord_admins)
    async def list(self, inter: ApplicationCommandInteraction, key: str, new_value: str):
        text = "Не удалось"
        thread_id = int(thread_id)
        async with aiosqlite.connect("MentionRolesThread.db", ) as db:
            await db.execute(
                f"INSERT INTO roles(role_id, thread_id, message_text)"
                f"VALUES ({role_id}, {thread_id}, '{message_text}')"
            )
            await db.commit()

            async with db.execute("SELECT * FROM roles WHERE id = (SELECT MAX(id) FROM roles)") as cursor:
                info = await cursor.fetchone()
                info = info[0]

                text = f"{text[0]}. <@&{text[1]}> -> <#{text[2]}> \n" \
                       f"╰ {text[3]} \n"

        await inter.send(text, ephemeral=True)

    @config.sub_command(name="список")
    @commands.check(discord_admins)
    async def list(self, inter: ApplicationCommandInteraction):
        async with aiosqlite.connect("MentionRolesThread.db", check_same_thread=False) as db:
            async with db.execute(f"SELECT * FROM roles") as cursor:
                row_list = await cursor.fetchall()

        full_text = ""
        for text in row_list:
            full_text += f"{text[0]}. <@&{text[1]}> -> <#{text[2]}> \n" \
                         f"╰ {text[3]} \n"

        await inter.send(full_text, ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(Config(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
