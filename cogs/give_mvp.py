from random import choice

from disnake.ext import commands
from disnake.ext.commands import Bot, Cog
from disnake import MessageCommandInteraction, Message, Embed


class MVPPlusPlusCog(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.message_command(name="Выдать MVP++")
    async def reverse(self, inter: MessageCommandInteraction, message: Message):
        mvppp_role_id = 610163742465982483
        mvp_role = message.guild.get_role(mvppp_role_id)
        await message.author.add_roles(mvp_role)
        colour_roles_ids = [
            937671345351839774, 937675436819873832, 937675633155248198, 937675708740808745, 937675806249996308,
            937675909194977330, 937675989499125820, 937676133166612540, 937676218441011211, 937676700806946837,
            937676332928761857, 937676481600045098
        ]
        colour_role = message.guild.get_role(choice(colour_roles_ids))
        await message.author.add_roles(colour_role)
        await message.channel.send(
            embed=Embed(
                title="Роль MVP++ выдана",
                description=f"{message.author.mention}, выдан <@&610163742465982483> и случайный цвет роли. "
                            "Его можно изменить при помощи </изменить-цвет:1010773661311053906>"
            )
        )
        await inter.response.send_message("Роль успешно выдана.", ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(MVPPlusPlusCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
