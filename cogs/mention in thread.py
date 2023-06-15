from disnake import ApplicationCommandInteraction, Member, Role
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog
import aiosqlite
from utils.checks import discord_admins

async def get_roles():
    try:
        async with aiosqlite.connect("MentionRolesThread.db", check_same_thread=False) as db:
            async with db.execute("SELECT role_id FROM roles") as cursor:
                thing = await cursor.fetchall()
                return thing

    except aiosqlite.Error as e:
        print(f"[ERROR {__name__}] {e}")


async def get_one(thing: str, role_id: str):
    async with aiosqlite.connect("MentionRolesThread.db", check_same_thread=False) as db:
        async with db.execute(f"SELECT {thing} FROM roles WHERE role_id = {role_id}") as cursor:
            thing = await cursor.fetchone()
            return thing[0]


class MentionRolesThread(Cog):
    """
    При появлении роли - пишет в канал. Работает с ветками.

    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    # Сам ивент срабатывания
    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        role_ids = await get_roles()
        for role_id in role_ids:
            role_id = role_id[0]

            if (before.get_role(role_id) is None) and (after.get_role(role_id) is not None):
                thread_id = await get_one("thread_id", role_id)
                thread = self.bot.get_channel(thread_id)
                message = await get_one("message_text", role_id)
                await thread.send(f"{after.mention}, {message}")

    @commands.slash_command(name="роль-упоминание")
    @commands.check(discord_admins)
    async def mention_roles_thread(self, inter: ApplicationCommandInteraction):
        pass

    @mention_roles_thread.sub_command(name="удалить")
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

    @mention_roles_thread.sub_command(name="добавить")
    @commands.check(discord_admins)
    async def list(self, inter: ApplicationCommandInteraction, role_id: Role, thread_id: str, message_text: str):
        text = "Не удалось"
        role_id = role_id.id
        thread_id = int(thread_id)
        async with aiosqlite.connect("MentionRolesThread.db", check_same_thread=False) as db:
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

    @mention_roles_thread.sub_command(name="список")
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
    bot.add_cog(MentionRolesThread(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
