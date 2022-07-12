# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands
from asyncio import TimeoutError


class StartUpMenu(disnake.ui.View):
    def __init__(self, embeds: list[disnake.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.page = 0

        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Страница {i + 1} из {len(self.embeds)}")

    @disnake.ui.button(emoji="<:back:990589488092807288>", style=disnake.ButtonStyle.secondary)
    async def prev_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.page -= 1
        embed = self.embeds[self.page]

        self.next_page.disabled = False
        if self.page == 0:
            self.prev_page.disabled = True
            self.add_item(disnake.ui.Button(label="Зайти на сервер", url="https://breadixpe.ru/play"))
        await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="<:next:990587920522031104>", style=disnake.ButtonStyle.secondary)
    async def next_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.page += 1
        embed = self.embeds[self.page]

        self.prev_page.disabled = False
        if self.page == len(self.embeds) - 1:
            self.next_page.disabled = True
        await inter.response.edit_message(embed=embed, view=self)


class Dropdown(disnake.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Нажмите чтобы выбрать роль гендера",
            min_values=1,
            max_values=1,
            options=[
                disnake.SelectOption(label="Женский", emoji=":female_sign:", value="0"),
                disnake.SelectOption(label="Мужской", emoji=":male_sign:", value="1"),
            ]
        )

    async def callback(self, inter: disnake.MessageInteraction):
        roles_id = [992760053503373442, 992760385167958046] #первая - женс, вторая - муж
        role = inter.guild.get_roles(roles_id[self.values[0]])
        await inter.user.add_roles(role)
        await inter.response.defer()


class InformationView(disnake.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @disnake.ui.button(emoji="<:rules:990587924615684107>", label="Правила",
                       style=disnake.ButtonStyle.blurple, custom_id="info:show_rules")
    async def show_rules(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(emoji="<:icon_clyde_white:992417678033690694>", label="Правила сообщества",
                                        style=disnake.ButtonStyle.url,
                                        url="https://discord.com/guidelines"))
        view.add_item(
            disnake.ui.Button(emoji="<:icon_clyde_white:992417678033690694>", label="Пользовательское соглашение",
                              style=disnake.ButtonStyle.url,
                              url="https://discord.com/terms"))
        rules_embed = disnake.Embed(
            title="Хей, голос, добавим суда правила?",
            description="Нарушения правил вёдет к наказанию. Наказание определяется администратором. \n • Наказания могут меняться с течением времени. Мы стараемся строить безопасное сообщество."
        )
        await inter.response.send_message(embed=rules_embed, view=view, ephemeral=True)

    @disnake.ui.button(emoji="<:start:990587922996666421>", label="Начать", style=disnake.ButtonStyle.green,
                       custom_id="info:start")
    async def start(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embeds = [
            disnake.Embed(
                title=":video_game: Игровые сервера",
                description="Для входа потребуется Minecraft: Pocket Edition версии 1.1.X ([например 1.1.5](https://www.google.ru/search?q=minecraft+PE+1.1.5)) \nМожно сыграть в такие режимы как: SkyWars, BedWars, Murder Mystery, Duels и Survival (Выживание) \n**IP:** play.breadixpe.ru \n**Port:** 19132"
            ).set_image(url="https://media.discordapp.net/attachments/925435932532936714/992768683887829073/Screenshot_82.png?width=840&height=473"),
            disnake.Embed(
                title="Ресурсы проекта",
                description=""
            ),
            disnake.Embed(
                title="Механики",
                description="Левелинг - говно, экономика жопа."
            )
        ]
        await inter.response.send_message(embed=embeds[0], view=StartUpMenu(embeds), ephemeral=True)

    @disnake.ui.button(emoji="<:edit:990587921776136272> ", label="Выбрать роли", style=disnake.ButtonStyle.gray,
                       custom_id="info:select_roles")
    async def select_roles(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embeds = [
            disnake.Embed(title=":zany_face: Выбрать роли",
                          description="ьно нажмите на одну из категорий ролей ниже, чтобы добавить роли, применимые к вам.")
        ]
        #Все люди разные! Чтобы украсить свой профиль и лучше понять вас и тип новостей, которые вы хотели бы получать, обязател
        await inter.response.send_message(embed=embeds[0], ephemeral=True)

    @disnake.ui.button(emoji="<:edit:990587921776136272> ", label="Обратиться", style=disnake.ButtonStyle.gray,
                       custom_id="info:apply")
    async def ticket_apply(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(
            title="Создать обращение",
            custom_id="create_ticket",
            components=[
                disnake.ui.TextInput(
                    label="Никнейм",
                    placeholder="Ведите ваш игровой никнейм (необязательно)",
                    custom_id="ticket:nickname",
                    style=disnake.TextInputStyle.short,
                    required=False,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Опишите причину",
                    placeholder="Предложение, жалоба, вопрос, заявка на роли. \nВы сможете ОТПРАВИТЬ ФОТО и добавить",
                    custom_id="ticket:reason",
                    style=disnake.TextInputStyle.paragraph,
                    min_length=5,
                    max_length=1024,
                ),
            ],
        )
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "create_ticket" and i.author.id == inter.author.id,
                timeout=300,
            )
        except TimeoutError:
            # Пользователь не отправил модальное сообщение в указанный период времени.
            # Discord не отправляет никаких событий, когда модальный объект закрыт / отклонен.
            return

        embed = disnake.Embed(title="Tag Creation")
        for custom_id, value in modal_inter.text_values.items():
            embed.add_field(name=custom_id.capitalize(), value=value, inline=False)

        from Bworld.cogs.tickets import create_ticket
        channel = await create_ticket(self.bot, inter.user, inter.user)
        await modal_inter.response.send_message(f"Ваш билетик: {channel.mention}", ephemeral=True)


class InformationChannelCog(commands.Cog):
    """Сообщение в канале информации"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.information_views_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")
        if not self.information_views_added:
            self.bot.add_view(InformationView(self.bot))
            self.information_views_added = True

    @commands.command()
    async def info(self, ctx: commands.Context):
        """Отправить сообщение"""
        info_embed = disnake.Embed(
            title=":sparkles: Добро пожаловать на BreadixWorld Discord!",
            description="""
Мы оффициальное сообщество BreadixWorld.
Здесь мы хотим объединить игроков нашего проекта.
*Общайтесь, слушайте музыку, найдите напарника, создайте клан, узнавайте новости, получите помощь и игровые монеты*! И просто приятно проведите время.

Кнопки под этим сообщением помогут вам: узнать правила, ознакомится с сервером и настроить себе роли.
""",
            color=None,
            colour=None
        )
        await ctx.send(embed=info_embed, view=InformationView(self.bot))


def setup(bot):
    bot.add_cog(InformationChannelCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
