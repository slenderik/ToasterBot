import datetime
import time

import aiosqlite
from aiosqlite import Error
from disnake import Embed
from disnake.ext import commands

create_users = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0
);
"""

create_discord_users = """
CREATE TABLE IF NOT EXISTS discord_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NID INTEGER NOT NULL,
    discord_id INTEGER NOT NULL,
    FOREIGN KEY (NID) REFERENCES users(NID) ON DELETE CASCADE
    CONSTRAINT discord_id_uq UNIQUE(discord_id)
);
"""

create_nicknames = """
CREATE TABLE IF NOT EXISTS nicknames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NID INTEGER NOT NULL,
    nickname TEXT UNIQUE NOT NULL,
    FOREIGN KEY (NID) REFERENCES users(NID) ON DELETE CASCADE,
    CONSTRAINT nickname_uq UNIQUE(nickname)
);
"""  # TODO CHECK


def get_nid(nid: list[list[int]]) -> int:
    nid = nid[0][0]
    return nid


def get_nicknames(nicknames: list[list[str]]) -> str:
    if nicknames is None:
        return None

    print(nicknames)
    result = ""
    for nickname in nicknames:
        result += f"{nickname[0]}, "

    return result[:-2]


async def add_nid_by_discord_id(discord_id: int):
    connect = await aiosqlite.connect("test.db")
    try:
        cursor = await connect.cursor()

        # if NID already exists
        await cursor.execute(f"SELECT NID FROM discord_users WHERE discord_id = {discord_id};")
        nid = await cursor.fetchall()
        if nid:
            return

        await cursor.execute("INSERT INTO users DEFAULT VALUES;")
        await connect.commit()
        await cursor.execute("SELECT NID FROM users WHERE NID = (SELECT MAX(NID) FROM users);")
        nid = await cursor.fetchall()
        nid = get_nid(nid)
        await cursor.execute(f"INSERT INTO discord_users(NID, discord_id) VALUES ({nid}, {discord_id});")
        await connect.commit()

    except Error as e:
        print(f"[ДОБАВИТЬ НИК АЙДИ ИЗ ДС АЙДИ] Ошибка: {e}")

    finally:
        await connect.close()


async def get_nid_by_discord_id(discord_id: int) -> int | None:
    connect = await aiosqlite.connect("test.db")
    nid = None
    try:
        cursor = await connect.cursor()
        await cursor.execute(f"SELECT NID FROM discord_users WHERE discord_id = {discord_id};")
        nid = await cursor.fetchall()
        nid = get_nid(nid)

    except Error as e:
        print(f"[ПОЛУЧИТЬ НИК АЙДИ ИЗ ДС АЙДИ] Ошибка: {e}")

    finally:
        await connect.close()

    return nid if nid else None


async def get_nicknames_by_discord_id(discord_id: int) -> list[str] | None:
    connect = await aiosqlite.connect("test.db")
    nicknames = None
    try:
        cursor = await connect.cursor()
        await cursor.execute(f"SELECT NID FROM discord_users WHERE discord_id = {discord_id};")
        nid = await cursor.fetchall()
        nid = get_nid(nid)

        await cursor.execute(f"SELECT nickname FROM nicknames WHERE nicknames.NID = {nid}")
        nicknames = await cursor.fetchall()
        print(f"nicknames: {nicknames}")
        await cursor.close()

    except Error as e:
        print(f"[ПОЛУЧИТЬ НИД ИЗ ДС ИД] Ошибка: {e}")

    finally:
        await connect.close()

    return nicknames if nicknames else None


async def get_nicknames_by_nid(nid: int) -> list[str] | None:
    connect = await aiosqlite.connect("test.db")
    nicknames = None
    try:
        cursor = await connect.cursor()
        await cursor.execute(f"SELECT nickname FROM nicknames WHERE nicknames.NID = {nid}")
        nicknames = await cursor.fetchall()
        print(f"nicknames: {nicknames}")
        await cursor.close()

    except Error as e:
        print(f"[ПОЛУЧИТЬ НИД ИЗ ДС ИД] Ошибка: {e}")

    finally:
        await connect.close()

    return nicknames if nicknames else None


async def get_nid_by_nickname(nickname: str) -> int | None:
    connect = await aiosqlite.connect("test.db")
    nid = None
    try:
        cursor = await connect.cursor()
        await cursor.execute(f"SELECT NID FROM nicknames"
                             f"WHERE nicknames.nickname = {nickname}")

        nid = await cursor.fetchall()
        nid = get_nid(nid)
        print(f"NID: {nid}")
        await cursor.close()
    except Error as e:
        print(f"[ПОЛУЧИТЬ НИД ИЗ ДС ИД] Ошибка: {e}")

    finally:
        await connect.close()

    return nid if nid else None


async def add_nicknames_by_nid(nid: int, names: list[str]) -> str | None:
    connect = await aiosqlite.connect("test.db")
    errors = ""
    for name in names:
        try:
            cursor = await connect.cursor()
            await cursor.execute(f"INSERT INTO nicknames (NID, nickname) VALUES ({nid}, '{name}');")

        except aiosqlite.IntegrityError as e:
            errors += f"\n Никнейм уже привязан. Обратитесь за помощью, для этого создайте обращение."

        # except Error as e:
        #     errors += f"\n {str(e)}"
        #     print(f"[ДОБАВИТЬ НИКИ ПО ДС ИД] Ошибка: {e}")

    await connect.commit()
    await connect.close()
    return errors if errors else None


class DBTest(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.command()
    async def profile(self, ctx: commands.Context):
        user = ctx.author

        await add_nid_by_discord_id(user.id)
        nid = await get_nid_by_discord_id(user.id)
        nicknames = await get_nicknames_by_nid(nid)
        nicknames = get_nicknames(nicknames)

        if nicknames is not None:
            nicknames = nicknames
        else:
            nicknames = f"У вас нет ещё привязанных никнеймов. Их можно привязать через команду" \
                        f"/nickname add (nicknames)` "
        embed = Embed(
            title="Профиль",
            description=f"**Общие сведения** \n"
                        f"> Пользователь: **{user.name} {user.discriminator}** \n"
                        f"> ID: `{user.id}` \n"
                        f"> Упоминание: {user.mention} \n"
                        f"> Создан: <t:{user.created_at}:R> \n"
                        f"> Цвет баннера: {user.banner}"
        )
        embed.add_field(
            name="Сервер",
            value=f"> Никнейкм: {user.nick} \n"
                  f"> Роль: {user.top_role.mention} \n"
                  f"> Присоединился: `{user.joined_at}",
            inline=False
        )
        embed.add_field(
            name="UNIDS",
            value=f"> NID: **{nid}** \n"
                  f"> Никнеймы: `{nicknames}`",
            inline=False
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.group()
    async def nickname(self, ctx: commands.Context):
        print("nicknames is invoked")

    @nickname.command()
    async def add(self, ctx: commands.Context, nicknames: str):
        await add_nid_by_discord_id(ctx.author.id)
        nid = await get_nid_by_discord_id(ctx.author.id)

        nicknames = nicknames.split(", ")
        errors = await add_nicknames_by_nid(nid, nicknames)

        if not errors:
            nicknames = await get_nicknames_by_nid(nid)
            nicknames = get_nicknames(nicknames)
            embed = Embed(
                title="Получилось! Никнеймы добавлены!",
                description=f"Ваши никнеймы: `{nicknames}`"
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="Ошибка!",
                description=f"{errors}"
            )
            await ctx.send(embed=embed)

    # @nickname.command()
    # async def find(self, ctx: commands.Context):
    #     NID = ctx.author.id
    #     main_id = await get_id_by_nickname(NID)
    #     nicknames = await get_nicknames_by_id(main_id)
    #
    #     if nicknames is None


def setup(bot: commands.Bot) -> None:
    bot.add_cog(DBTest(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
