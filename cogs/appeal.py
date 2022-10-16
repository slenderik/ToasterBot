import calendar
import datetime
from asyncio import sleep

import disnake
from disnake.ext import commands


class Confirm(disnake.ui.View):
    def __init__(self, user):
        super().__init__()
        self.user = None

    @disnake.ui.button(label="Разблокировать", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.stop()

    @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.grey)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("Cancelling", ephemeral=True)

        self.stop()


class AppealView(disnake.ui.View):
    def __init__(self, user: disnake.User):
        super().__init__()
        self.user = user

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        confirm_embed = disnake.Embed(
            title="Участник разблокирован",
            description=f"Разблокирован: {user.mention}"
                        f"Причина бана: "
                        f"Апелляция: {inter.response.original_message}"
        )
        await inter
        await inter.response.send_message("Confirming", embed=confirm_embed, ephemeral=True)
        self.stop()

    @disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.red)
    async def cancel_appeal(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        cancel_embed = Em
        await inter.response.send_message("Апелляция отклонена", ephemeral=True)

        self.stop()


class AppealModal(disnake.ui.Modal):

    def __init__(self) -> None:
        components = [
            disnake.ui.TextInput(
                label="Объяснительная",
                placeholder="The content of the tag",
                custom_id="Объяснительная",
                style=disnake.TextInputStyle.paragraph,
                min_length=5,
                max_length=1024,
            ),
        ]
        super().__init__(title="Запросить разблокировку", custom_id="appeal:modal", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        embed = disnake.Embed(title="Апелляция")
        for key, value in inter.text_values.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await inter.response.send_message(embed=embed)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        await inter.response.send_message("Что-то пошло ни так. Заполните форму заново", ephemeral=True)


def get_appeal_cooldown(reason: str) -> str | None:
    if "Апелляция" not in reason:
        return None
    else:
        index = reason.rfind("Апелляция")
        time = reason[index:]
        return time


class AppealCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(auto_sync=True, name="подать-апелляцию", dm_permission=True)
    async def appeal_give(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Апелляция подана")
        await sleep(5)
        message = await inter.original_message()
        await message.edit(f"{inter.user.mention} Апелляция не принята")

    @commands.slash_command(auto_sync=True, name="запросить", dm_permission=True)
    async def request(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @request.sub_command(auto_sync=True, name="разблокировку")
    async def unblocking(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_modal(modal=AppealModal())

    @commands.command()
    async def ban(self, ctx: commands.Context, user: disnake.User):
        date = datetime.datetime.now()
        months = 5  # ВРЕМЯ ОТКАТА
        month = date.month - 1 + months
        year = date.year + month // 12
        month = month % 12 + 1
        day = min(date.day, calendar.monthrange(year, month)[1])
        date = datetime.date(year, month, day)
        await ctx.send(f"{date} <t:{datetime.date(year, month, day).timestamp()}>")

        # guild = await self.bot.get_guild(guild_id)
        # await guild.unban(user, reason="")
        # await guild.ban(user, reason="")

    @commands.command()
    async def is_ban(self, ctx: commands.Context, user: disnake.User):
        ban_status = False
        reason = None
        async for ban in ctx.guild.bans(limit=None):
            if ban.user.id == user.id:
                ban_status = True
                reason = ban.reason
                break

        time = get_appeal_cooldown(reason)

        if ban_status is True:
            await ctx.send(f"{user.mention} is banned \n"
                           f"reason: {reason} \n"
                           f"time = {time}")
        else:
            await ctx.send(f"{user.mention} is not banned")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AppealCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
