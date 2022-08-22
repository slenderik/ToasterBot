# noinspection PyUnresolvedReferences
from enum import Enum

import disnake
from disnake import Embed
from disnake.ext import commands


class PlayButton(disnake.ui.View):

    def __init__(self, embed: disnake.Embed, author: disnake.User):
        super().__init__(timeout=180)
        self.author = author
        self.embed = embed
        self.members = []

    @disnake.ui.button(label="Я тоже хочу!", style=disnake.ButtonStyle.blurple)
    async def me_too(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id == self.author.id:
            await inter.response.send_message(embed=disnake.Embed(title="Вы не можете это использовать, так как сами "
                                                                        "предложили. Эта кнопка для других "
                                                                        "участников!"), ephemeral=True)
            return

        if inter.user.id not in self.members:  # первый раз нажал
            self.members.append(inter.user.id)
        else:  # вторично нажал
            self.members.remove(inter.user.id)

        if self.members:
            # Обновляем список желающих
            try:
                self.embed.remove_field(0)
            finally:
                text = ""
                for member in self.members:
                    text += f"<@{member}>\n"

                self.embed.add_field(name="Хотят сыграть", value=text)
        else:
            # никого нет - удалить список
            self.embed.remove_field(0)

        await inter.response.edit_message(embed=self.embed)


class ChatCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="предложить")
    async def offer(self, inter: disnake.ApplicationCommandInteraction):
        pass

    Servers = commands.option_enum(
        ["SkyWars №1", "SkyWars №2", "SkyWars №3", "BedWars №1", "BedWars №2", "BedWars №3", "Duels №1",
         "Murder Mystery №1", "Murder Mystery №2", "Survival №1"])

    @offer.sub_command(name="поиграть")
    @commands.cooldown(2, 360.0, commands.BucketType.user)
    async def to_play(self, inter: disnake.ApplicationCommandInteraction, сервер: Servers = None):
        """
        Предложите сыграть, кто-то откликнется!
        Parameters
        ----------
        сервер: либо выберите сервер!
        """
        offer_embed = Embed(title="Предлагает сыграть!" if сервер is None else f"Предлагает сыграть на {сервер}!")
        offer_embed.set_author(name=inter.user.display_name, icon_url=inter.user.display_avatar.url)
        view = PlayButton(embed=offer_embed, author=inter.user)
        await inter.response.send_message(embed=offer_embed, view=view, delete_after=360.0)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ChatCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")