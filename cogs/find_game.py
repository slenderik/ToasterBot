import disnake
from disnake import Embed, permissions, MessageInteraction, ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ui import Button

from utils.config import servers


class PlayButton(disnake.ui.View):

    def __init__(self, embed: Embed, author: disnake.User):
        super().__init__(timeout=180)
        self.author = author
        self.embed = embed
        self.members = []

    @disnake.ui.button(label="Буду играть", style=disnake.ButtonStyle.green)
    async def me_too(self, button: Button, inter: MessageInteraction):
        if inter.user.id == self.author.id:
            await inter.response.send_message("Вы предложили другим участникам поиграть, поэтому не можете это нажать. "
                                              "Эта кнопка для других участников.", ephemeral=True)
            return

        if inter.user.id not in self.members:  # добавляем в желающих
            self.members.append(inter.user.id)

        else:
            self.members.remove(inter.user.id)  # убираем в желающих

        if self.members:  # Обновляем список желающих
            try:
                self.embed.remove_field(0)
            finally:
                text = ""
                for member in self.members:
                    text += f"<@{member}>\n"

                self.embed.add_field(name="Будут играть", value=text)
        else:
            # никого нет - удалить список
            self.embed.remove_field(0)

        await inter.response.edit_message(embed=self.embed)

    @disnake.ui.button(emoji="🗑️", style=disnake.ButtonStyle.gray)
    async def delete(self, button: Button, inter: MessageInteraction):
        if inter.user.id == self.author.id:
            text = ""
            for member_id in self.members:
                text += f"<@{member_id}>, "
            text = f"Для игры найдены: {text[:2]}" if self.members else "Никто не найден"
            await inter.message.delete()
            await inter.response.send_message(embed=Embed(title="Сообщение удалено.", description=text), ephemeral=True)

        elif inter.user.guild_permissions.manage_messages:
            await inter.message.delete()
            await inter.response.send_message("Сообщение удалено.", ephemeral=True)

        elif inter.user.id != self.author.id:
            await inter.response.send_message("Это сообщение может удалить только его автор.", ephemeral=True)


class ChatCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="найти")
    async def offer(self, inter: ApplicationCommandInteraction):
        pass

    Servers = commands.option_enum(servers)

    @offer.sub_command(name="игру")
    @commands.cooldown(2, 360.0, commands.BucketType.user)
    async def to_play(self, inter: ApplicationCommandInteraction, режим: Servers = None):
        """
        Найти людей для совместной игры
        Parameters
        ----------
        режим: Выберите сервер для игры
        """
        offer_embed = Embed(colour=0x2d7d46)
        if режим is None:
            offer_embed.set_author(
                name=f"{inter.user.display_name} ищет игроков для игры",
                icon_url=inter.user.display_avatar.url
            )
        else:
            offer_embed.set_author(
                name=f"{inter.user.display_name} ищет игроков для игры {режим}",
                icon_url=inter.user.display_avatar.url
            )
        view = PlayButton(embed=offer_embed, author=inter.user)
        await inter.response.send_message(embed=offer_embed, view=view, delete_after=360.0)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ChatCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
