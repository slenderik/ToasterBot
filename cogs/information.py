# noinspection PyUnresolvedReferences
import disnake
from disnake import Embed, SelectOption
from disnake.ext import commands
from disnake.ui import Button


class GuideMenu(disnake.ui.View):
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
            max_values=1,
            options=[
                disnake.SelectOption(label="Женский", emoji=":female_sign:", value="0"),
                disnake.SelectOption(label="Мужской", emoji=":male_sign:", value="1"),
            ]
        )

    async def callback(self, inter: disnake.MessageInteraction):
        roles_id = [992760053503373442, 992760385167958046]  # первая - женс, вторая - муж
        role = inter.guild.get_roles(roles_id[self.values[0]])
        await inter.user.add_roles(role)
        await inter.response.defer()


async def delete_roles(member: disnake.Member, roles: list):
    for role in roles:
        if role in member.roles:
            await member.delete_role()

        continue


class NotificationsSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            SelectOption(
                label="SkyWars №1",
                description="Если собираетесь тут играть",
                emoji="🟦"
            ),
        ]

        super().__init__(
            placeholder="Нажмите, чтобы выбрать уведомления!",
            custom_id="roles:notifications",
            max_values=1,
            row=1,
            options=options
        )

    async def callback(self, inter: disnake.MessageInteraction):
        ...


class CustomizeRoles(disnake.ui.View):

    def __init__(self, main_embed):
        super().__init__(timeout=None)
        self.main_embed = main_embed
        self.add_item(SelectServer())

    @disnake.ui.button(label="Уведомления", style=disnake.ButtonStyle.blurple, custom_id="roles:notifications")
    async def notifications(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.original_message_edit(view=None, ephemeral=True)

    @disnake.ui.button(label="Устройства", style=disnake.ButtonStyle.blurple, custom_id="roles:devices")
    async def devices(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        ...

    @disnake.ui.button(label="Любимые режимы", style=disnake.ButtonStyle.blurple, custom_id="roles:game_modes")
    async def game_modes(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        ...

    @disnake.ui.button(label="Гендер", style=disnake.ButtonStyle.blurple, custom_id="roles:gender")
    async def gender(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        ...


# class InfoView(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#
#     @disnake.ui.button(emoji="<:rules:990587924615684107>", label="Правила",
#                        style=disnake.ButtonStyle.blurple, custom_id="info:show_rules")
#     async def show_rules(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
#         view = disnake.ui.View()
#         view.add_item(
#             disnake.ui.Button(
#                 emoji="<:icon_clyde_white:992417678033690694>",
#                 label="Правила сообщества",
#                 style=disnake.ButtonStyle.url,
#                 url="https://discord.com/guidelines"
#             )
#         )
#         view.add_item(
#             disnake.ui.Button(
#                 emoji="<:icon_clyde_white:992417678033690694>",
#                 label="Пользовательское соглашение",
#                 style=disnake.ButtonStyle.url,
#                 url="https://discord.com/terms"
#             )
#         )
#         rules_embed = disnake.Embed(
#             title="Хей, голос, добавим суда правила?",
#             description="Нарушения правил вёдет к наказанию. Наказание определяется администратором. \n • Наказания "
#                         "могут меняться с течением времени. Мы стараемся строить безопасное сообщество. "
#         )
#         await inter.response.send_message(embed=rules_embed, view=view, ephemeral=True)
#
#     @disnake.ui.button(emoji="<:start:990587922996666421>", label="Начать",
#                        style=disnake.ButtonStyle.green, custom_id="info:start")
#     async def start(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
#         embeds = [
#             disnake.Embed(
#                 title=":video_game: Игровые сервера",
#                 description="Для входа потребуется Minecraft: Pocket Edition версии 1.1.X ([например 1.1.5]("
#                             "https://www.google.ru/search?q=minecraft+PE+1.1.5)) \nМожно сыграть в такие режимы как: "
#                             "SkyWars, BedWars, Murder Mystery, Duels и Survival (Выживание) \n**IP:** "
#                             "play.breadixpe.ru \n**Port:** 19132 "
#             ).set_image(
#                 url="https://media.discordapp.net/attachments/925435932532936714/992768683887829073/Screenshot_82.png"
#                     "?width=840&height=473"),
#             disnake.Embed(
#                 title="Ресурсы проекта",
#                 description=""
#             ),
#             disnake.Embed(
#                 title="Механики",
#                 description="Левелинг - говно, экономика жопа."
#             )
#         ]
#         await inter.response.send_message(embed=embeds[0], view=GuideMenu(embeds), ephemeral=True)
#
#     @disnake.ui.button(emoji="<:edit:990587921776136272> ", label="Выбрать роли",
#                        style=disnake.ButtonStyle.gray, custom_id="info:select_roles")
#     async def select_roles(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
#         roles_embed = Embed(
#             title=":zany_face: Выберите себе роле ",
#             description="Все люди разные! Чтобы украсить свой профиль и лучше понять вас и тип новостей, которые вы "
#                         "хотели бы получать, обязательно нажмите на одну из категорий ролей ниже, чтобы добавить роли, "
#                         "применимые к вам. "
#         )
#         await inter.response.send_message(embed=roles_embed, view=CustomizeRoles(roles_embed), ephemeral=True)
#
#     @disnake.ui.button(emoji="<:edit:990587921776136272> ", label="Обратиться",
#                        style=disnake.ButtonStyle.gray, custom_id="info:ticket_apply")
#     async def ticket_apply(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
#         from cogs.tickets import TicketModal
#         modal = TicketModal()
#         await inter.response.send_modal(modal=modal)

cooldown_ticket = {}


class InfoCog(commands.Cog):
    """Сообщение в канале информации"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.information_views_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")
        if not self.information_views_added:
            self.information_views_added = True

    @commands.command()
    async def info(self, ctx: commands.Context):
        """Отправить сообщение"""
        text = "Мы официальное сообщество BreadixWorld. \n" \
               "Здесь мы хотим объединить игроков нашего проекта. \n" \
               "*Общайтесь, слушайте музыку, найдите напарника, создайте клан, узнавайте новости, получите " \
               "помощь и игровые монеты*! И просто приятно проведите время. \n\n" \
               "Кнопки под этим сообщением помогут вам: узнать правила, ознакомится с сервером и настроить себе роли."

        info_embed = Embed(
            title=":sparkles: Добро пожаловать на BreadixWorld Discord!",
            description=text,
            color=None,
            colour=None
        )

        components = [
            Button(emoji="<:rules:990587924615684107>", label="Правила",
                   style=disnake.ButtonStyle.blurple, custom_id="info:show_rules"),
            Button(emoji="<:start:990587922996666421>", label="Начать",
                   style=disnake.ButtonStyle.green, custom_id="info:start"),
            Button(emoji="<:edit:990587921776136272> ", label="Выбрать роли",
                   style=disnake.ButtonStyle.gray, custom_id="info:select_roles"),
            Button(emoji="<:edit:990587921776136272> ", label="Обратиться",
                   style=disnake.ButtonStyle.gray, custom_id="info:ticket_apply")
        ]
        await ctx.send(embed=info_embed, components=components)

    @commands.Cog.listener("on_button_click")
    async def voices_buttons_listener(self, inter: disnake.MessageInteraction):
        button_id = inter.component.custom_id
        if button_id.startswith("info"):
            if button_id == "info:show_rules":
                from cogs.rules import rules_texts, number_of_rules
                rules_embed = Embed(title="Правила сообщества в Discord")
                for clause in range(1, number_of_rules + 1):
                    rules_embed.add_field(
                        name=f"{clause}. {rules_texts[str(clause) + '_заголовок']}",
                        value=rules_texts[str(clause) + '_содержание'],
                        inline=False
                    )
                rules_embed.set_footer(text="Некоторые ситуации могут решаться на усмотрение администратора.")

                await inter.response.send_message(embed=rules_embed, ephemeral=True)

            elif button_id == "info:start":
                await inter.response.send_message("0w31023981", ephemeral=True)

            elif button_id == "info:select_roles":
                roles_embed = Embed(
                    title=":zany_face: Выберите себе роли",
                    description="Все люди разные! Чтобы украсить свой профиль и лучше понять вас и тип новостей, "
                                "которые вы хотели бы получать, обязательно нажмите на одну из категорий ролей ниже, "
                                "чтобы добавить роли, применимые к вам. "
                )

                components = [
                    Button(label="Уведомления", style=disnake.ButtonStyle.blurple, custom_id="roles:notifications"),
                    Button(label="Устройства", style=disnake.ButtonStyle.blurple, custom_id="roles:devices"),
                    Button(label="Любимые режимы", style=disnake.ButtonStyle.blurple, custom_id="roles:game_modes"),
                    Button(label="Гендер", style=disnake.ButtonStyle.blurple, custom_id="roles:gender"),
                ]

                await inter.response.send_message(embed=roles_embed, components=components, ephemeral=True)

            elif button_id == "info:ticket_apply":
                from extension.cooldown import cooldown_time, is_cooldown, add_cooldown
                print(inter.user.id, cooldown_ticket)
                if is_cooldown(inter.user.id, cooldown_ticket):
                    cooldown = await cooldown_time(member.id, cooldown_ticket)
                    await after.channel.send(
                        f"{inter.user.mention}, Используйте через {cooldown} сек!",
                        delete_after=cooldown
                    )
                    return

                from cogs.tickets import TicketModal
                modal = TicketModal()
                await inter.response.send_modal(modal=modal)
                print('1 ads')
                await add_cooldown(inter.user.id, cooldown_ticket, 300)
                print('2 ads')

        elif button_id.startswith("roles"):
            if button_id == "roles:notifications":
                pass

            elif button_id == "roles:devices":
                pass

            elif button_id == "roles:game_modes":
                pass

            elif button_id == "roles:gender":
                pass

        elif button_id:
            await inter.response.send_message(f"Неизвестный custom_id: {button_id}")
        else:
            await inter.response.send_message(f"Пока что не понятно как ты это сделал.\nОшибка: {inter.component}")


def setup(bot):
    bot.add_cog(InfoCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
