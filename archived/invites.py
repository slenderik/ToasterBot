from asyncio import sleep
from datetime import datetime

from disnake import Invite, Member, Embed
from disnake.ext import commands

from utils.config import guild_id

invites = {}


def get_embed(name: str, invite: Invite, color: int = None, member: Member = None):
    if invite.created_at is not None:
        created_time = f"<t:{round(invite.created_at.timestamp())}> <t:{round(invite.created_at.timestamp())}:R>"
    else:
        created_time = "`Не известно`"

    if invite.expires_at is not None:
        expires_time = f"<t:{round(invite.expires_at.timestamp())}> <t:{round(invite.expires_at.timestamp())}:R>"
    else:
        expires_time = "`∞`"

    if invite.temporary is True:
        temporary = f"Временное. Приглашённые участники будут удалены после выключении ссылки"
    else:
        temporary = "`Навсегда`"

    convert_time = {
        0: "∞",
        1800: "30 минут",
        3600: "1 час",
        21600: "6 часов",
        43200: "12 часов",
        86400: "1 день",
        604800: "7 дней (неделя)"
    }
    time = f"`{convert_time[invite.max_age]}`" if invite.max_age is not None else "`Не известно`"
    channel = f"{invite.channel.mention} `{invite.channel.name}`" if invite.channel is not None else "`Не известно`"
    creator = invite.inviter.mention if invite.inviter is not None else "`Не известно`"
    max_usage = invite.max_uses if invite.max_uses != 0 else "∞"
    uses = f"`{invite.uses} / {max_usage}`" if invite.uses is not None else "`Не известно`"

    embed = Embed(
        title=name,
        color=color,
        timestamp=datetime.now()
    )
    event_name = "`Не известно`" if invite.guild_scheduled_event is None else f"`{invite.guild_scheduled_event.name}`"
    event_status = "`Не известно`" if invite.guild_scheduled_event is None else f"`{invite.guild_scheduled_event.status}`"
    application = "Не известно" if invite.target_application is None else invite.target_application
    welcome_screen = "Не известно" if invite.guild_welcome_screen is None else invite.guild_welcome_screen.enabled
    embed.add_field(
        name="Гильдия",
        value=f"```{invite.guild.name}```"
              f"Участников: {invite.approximate_member_count} Активных: {invite.approximate_presence_count} \n"
              f"Ивент: {event_name} Статус: {event_status} \n"
              f"Приложение: `{application}` \n"
              f"Экран приветствия: `{welcome_screen}` \n"
              f"Тип: `{invite.target_type}` Пользователь: `{invite.target_user}` \n",
        inline=False
    )
    if member is None:
        embed.add_field(
            name="Приглашение",
            value=f"```{invite.url}```"
                  f"Создатель: {creator} \n"
                  f"Канал: {channel} \n"
                  f"От: {created_time} \n"
                  f"До: {expires_time} \n"
                  f"Время: {time}\n"
                  f"Вход: {temporary} \n"
                  f"Использований: {uses}",
            inline=False
        )
    elif member is not None:
        create_time = f"<t:{round(member.created_at.timestamp())}> <t:{round(member.created_at.timestamp())}:R>"
        join_time = f"<t:{round(member.joined_at.timestamp())}> <t:{round(member.joined_at.timestamp())}:R>"
        embed.add_field(
            name="Участник",
            value=f"```{member.name}#{member.discriminator} ({member.display_name}#{member.discriminator})```\n"
                  f"Упоминание: {member.mention} \n"
                  f"ID: `{member.id}` \n"
                  f"Создан: {created_time}\n"
                  f"Зашёл: {join_time}",
            inline=False
        ).add_field(
            name="Приглашение",
            value=f"```{invite.url}```"
                  f"Пригласил: {creator} \n"
                  f"Канал: {channel} \n"
                  f"От: {created_time} \n"
                  f"До: {expires_time} \n"
                  f"Время: {time} \n"
                  f"Вход: {temporary} \n"
                  f"Использований: `{invite.uses} / {max_usage}`",
            inline=False
        )
    return embed


class InvitesCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")
        # add all invites
        guild = self.bot.get_guild(guild_id)
        new_invites = await guild.invites()
        for invite in new_invites:
            if invite.code not in invites:
                invites.update({invite.code: invite})

    @commands.Cog.listener()
    async def on_invite_create(self, invite: Invite):
        invites.update({invite.code: invite})

        invite_create_embed = get_embed(name="Приглашение было создано", color=0x36CE36, invite=invite)
        from utils.logging import log_send
        await log_send(self.bot, invite_create_embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: Invite):
        invite_delete_embed = get_embed(name="Приглашение было удалено", color=0xCE3636, invite=invites[invite.code])
        from utils.logging import log_send
        await log_send(self.bot, invite_delete_embed)

        if invite.code in invites:
            await sleep(10)
            invites.pop(invite.code)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        guild = self.bot.get_guild(guild_id)
        new_invites = await guild.invites()
        invite_code = None
        new_codes = [i.code for i in new_invites]

        for invite in list(invites):
            if invite not in new_codes:
                invite_code = invites[invite]

        for new_invite in new_invites:
            if new_invite.code in invites and new_invite.uses > invites[new_invite.code].uses:
                invite_code = new_invite

            invites.update({new_invite.code: new_invite})

        member_join_embed = get_embed(name="Новый участник!", member=member, invite=invite_code)

        from utils.logging import log_send
        await log_send(self.bot, member_join_embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(InvitesCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
