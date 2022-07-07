# noinspection PyUnresolvedReferences
from enum import Enum

import disnake
from disnake import Embed
from disnake.ext import commands


class PlayButton(disnake.ui.View):
    def __init__(self, embed: disnake.Embed):
        super().__init__(timeout=180)
        self.embed = embed
        self.members = []

    @disnake.ui.button(label="Я тоже хочу!", style=disnake.ButtonStyle.blurple)
    async def i_want_to_play(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        # Если пользователь первый раз нажал
        if inter.user.mention not in self.members:
            self.members.append(inter.user.mention)
        # Если пользователь вторично нажал
        elif inter.user.mention in self.members:
            self.members.remove(inter.user.mention)
        # Если пользователей больше нет
        if self.members == []:
            self.embed.remove_field(0)
        # Если пользователи есть
        else:
            # Обновляем список желающих
            try:
                self.embed.remove_field(0)
            finally:
                text = ""
                for member in self.members:
                    text += f"{member}\n"
                self.embed.add_field(
                    name="Хотят сыграть",
                    value=text
                )
        await inter.response.edit_message(embed=self.embed)


class ChatCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="хотите")
    async def offer(self, inter: disnake.ApplicationCommandInteraction):
        pass

    Servers = commands.option_enum(
        ["BedWars №1", "BedWars №2", "BedWars#3", "SkyWars №1", "SkyWars №2", "SkyWars №3", "Murder Mystery №1",
         "Murder Mystery №2", "Survival №1", "Duels №1"])

    @offer.sub_command(name="сыграть")
    @commands.cooldown(2, 360.0, commands.BucketType.user)
    async def to_play(self, inter: disnake.ApplicationCommandInteraction, сервер: Servers):
        """
        Предложите сыграть где-нибудь. Кто-то откликнется!
        Parameters
        ----------ц
        сервер: Либо предложите сыграть на определённом сервере!
        """
        text = "Предлагает сыграть!" if сервер is None else f"Предлагает сыграть на {сервер}!"

        offer_embed = Embed(title=text)
        offer_embed.set_author(
            name=inter.user.display_name,
            icon_url=inter.user.display_avatar.url
        )
        await inter.response.send_message(embed=offer_embed, view=PlayButton(embed=offer_embed), delete_after=360.0)


def setup(bot):
    bot.add_cog(ChatCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
