import disnake
from disnake.ext import commands

guild_id = 823820166478823462
channel_id = 1010604701454180453


class InvitesCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.invites = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")
        guild = self.bot.get_guild(guild_id)
        invites = await guild.invites()
        for invite in invites:
            if invite.code not in self.invites:
                self.invites.update({invite.code: invite})

        print(self.invites)

    @commands.Cog.listener()
    async def on_invite_create(self, invite: disnake.Invite):
        # TODO сообщение в логи
        print(self.invites)
        print(invite.code)
        self.invites.update({invite.code: invite})
        print(self.invites)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: disnake.Invite):
        # TODO сообщение в логи
        print(self.invites)
        print(invite.code)
        if invite.code in self.invites:
            await asyncio.sleep(10)
            invites.pop(invite.code)
            print(self.invites)

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        guild = self.bot.get_guild(guild_id)
        new_invites = await guild.invites()
        invites = self.invites
        invite_code = None
        print(invites)

        print(new_invites)
        new_codes = [i.code for i in new_invites]
        print(new_codes)

        for invite in list(invites):
            if invite not in new_codes:
                print(f"1. {invite}")
                print(f"2. {invite not in new_codes}")
                invite_code = invites[invite]

        print(f"ИНВАЙТ: {invite_code}")
        print('_____________________________')

        for new_invite in new_invites:
            print(f"1. {new_invite.code}")
            print(f"2. {new_invite.uses}")
            print(f"3. {invites[new_invite.code]}")
            print(f"4. {invites[new_invite.code].code}")

            if new_invite.code in invites and new_invite.uses > invites[new_invite.code].uses:
                print(f"Было: {invites[new_invite.code].uses}")
                print(f"Стало: {new_invite.uses}")
                print(new_invite.uses > invites[new_invite.code].uses)
                invite_code = new_invite

            # elif new_invite.code not in invites:
            #     print(f"1. {new_invite.code}")
            #     print(f"2. {invites}")
            #     print(f" {new_invite.code not in invites}")
            #     invite_code = new_invite
            invites.update({new_invite.code: new_invite})

            print(f"ИНВАЙТ: {invite_code}")
            print('_____________________________')

        print(f"ИНВАЙТ: {invite_code}")

        embed = disnake.Embed(
            title="Новый участник!",
            description=f"Я учусь отслеживать участников"
        ).add_field(
            name="Участник",
            value=f"**{member.name}#{member.discriminator}** ({member.display_name}#{member.discriminator}) \n"
                  f"Упоминание: {member.mention} \n"
                  f"ID: `{member.id}` \n"
                  f"Создан: <t:{round(member.created_at.timestamp())}> (<t:{round(member.created_at.timestamp())}:R>)\n"
                  f"Зашёл: <t:{round(member.joined_at.timestamp())}> (<t:{round(member.joined_at.timestamp())}:R>)",
            inline=False
        )

        if invite_code is not None:
            embed.add_field(
                name="Приглашение",
                value=f"```{invite_code.url}```"
                      f"Приглашён: {invite_code.inviter.mention} \n"
                      f"Создано: <t:{round(invite_code.created_at.timestamp())}:R> \n"
                      f"Использований: {invite_code.uses} / {invite_code.max_uses}",
                inline=False
            )

        channel = guild.get_channel(channel_id)
        await channel.send(embed=embed)
        print(invites)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(InvitesCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
