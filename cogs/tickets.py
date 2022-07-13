# noinspection PyUnresolvedReferences
import time
import datetime
import disnake
from disnake.ext import commands


async def ticket_count(category) -> int:
    """Вернуть номер тикета"""
    n = category.text_channels
    if not n:
        return 1
    n = str(n[len(n) - 1])
    if n[1:2] == "︱":
        n = int(n[:1])
        n += 1
    else:
        n = int(n[:2])
        n += 1
    return n


async def create_ticket_and_return_channel(bot, user, creator=None, embed=None) -> object:
    """Создать канал обращения и вернуть канал"""
    category = bot.get_channel(940666384734646292)  # CATEGOTY ID HERE
    permission = {
        user: disnake.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, read_message_history=True)
    }
    if creator is None:
        channel = await category.create_text_channel(
            name=f"{await ticket_count(category)}︱{user.display_name}",
            overwrites=permission,
            topic=f":penguin: **Информация** \nСоздан: **{user.name}** ({user.id}) \nВремя: <t:{round(time.mktime(datetime.datetime.now().timetuple()))}:R>",
            reason=f"{user.name}({user.id})"
        )
    else:
        channel = await category.create_text_channel(
            name=f"{await ticket_count(category)}︱{user.display_name}",
            overwrites=permission,
            topic=f":penguin: **Информация** \n\nСоздан: **{creator.name}** ({creator.id}) \nДля: **{user.name}** ({user.id}) \nВремя: <t:{round(time.mktime(datetime.datetime.now().timetuple()))}:R>",
            reason=f"{creator.name}({creator.id})"
        )
    await channel.send(f"Hey, {user.mention}", embed=embed)
    return channel


class TicketsCog(commands.Cog):
    """Дополнение обращений"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.message_command(name="Создать билетик")
    @disnake.ext.commands.has_role(977974127304515614)
    async def ticket(self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
        """Создать канал обращения"""
        user = message.author
        if user.bot:
            await inter.response.send_message(f"Hey, {inter.user.mention}. {user.mention} это бот!", ephemeral=True)
        else:
            channel = await create_ticket(self.bot, inter.user, message.author)
            await inter.response.send_message(
                embed=disnake.Embed(
                    title="🎫 Билетик создан",
                    description=f"Для: {user.mention} ({user.id}) \nКанал: {channel.mention}"),
                ephemeral=True
            )

    # @ticket.error
    # async def tickets(self, inter: disnake.ApplicationCommandInteraction, error):
    #     if isinstance(error, commands.MissingRole):


def setup(bot):
    bot.add_cog(TicketsCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
