# выключить NSFW, очистить чат войса, удалить и создать войс
from asyncio import sleep, TimeoutError
from random import choice
from time import time
from disnake import SelectOption

import disnake
import asyncio
from disnake.ext import commands
from disnake.utils import get

voice_create_id = 997851742475669594
server_id = 823820166478823462
logo_url = "https://media.discordapp.net/attachments/925973441524424716/925973455919251536/logo_bread.png?width=473" \
           "&height=473 "

custom_rooms = {}


async def channel_name(name: str) -> str:
    """Вернуть название канала с учётом разных штук."""
    if "🔞" in name:
        name = f"[🔞] {name}"
    return name


async def get_channel(guild: object, user_id: int) -> object | None:
    """Вернуть канал автора."""
    return get(guild.voice_channels, id=custom_rooms[user_id]) if custom_rooms.get(user_id, None) is not None else None


async def disable(self: object, button: disnake.ui.Button, inter: disnake.MessageInteraction):
    """Отключить нажатую кнопку."""
    # включаем все кнопки в том же ряду
    for child in self.children:
        if isinstance(child, disnake.ui.Button):
            if child.row == button.row:
                child.disabled = False
    # выключаем нажатую кнопку
    button.disabled = True
    await inter.response.edit_message(view=self)


cooldowns = {}


async def cooldown_time(user_id: int) -> str:
    """"Вернуть время на кулдаун."""
    if cooldowns.get(user_id, None) is not None:
        cooldown = str(cooldowns[user_id] - round(time()))
    else:
        cooldown = "0 UwU"
    return cooldown


async def is_cooldown(user_id: int) -> bool:
    """"Вернуть значение, находится ли пользователь в кулдауне."""
    return bool(cooldowns.get(user_id, None))


async def add_cooldown(user_id: int, time_: int = 30):
    """Добавить в кулдауны время когда участник сможет использовать команду снова."""
    cooldown: int = round(time())
    cooldown += time_  # время отката/кулдауна
    cooldown = {user_id: cooldown}
    cooldowns.update(cooldown)
    await sleep(time_)
    cooldowns.pop(user_id)


class SettingsView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(custom_id="voice_view:yes_profanity", emoji="🔞", label="С матом", style=disnake.ButtonStyle.red,
                       row=2)
    async def yes_profanity(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        await channel.edit(name=f"[🔞] {channel.name}", reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(custom_id="voice_view:no_profanity", emoji="🔞", label="Без мата", style=disnake.ButtonStyle.red,
                       row=2)
    async def no_profanity(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        await channel.edit(name=channel.name[4:], nsfw=True, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(custom_id="voice_view:unlock_channel", emoji="🔓", label="Открыть",
                       style=disnake.ButtonStyle.blurple,
                       row=3)
    async def unlock_channel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        user = inter.user
        overwrites = {user: disnake.PermissionOverwrite(view_channel=True, manage_channels=True)}
        await channel.edit(overwrites=overwrites, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(custom_id="voice_view:lock_channel", emoji="🔒", label="Закрыть",
                       style=disnake.ButtonStyle.blurple, row=3)
    async def lock_channel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)


class LimitView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="1", custom_id="limit:1", style=disnake.ButtonStyle.blurple)
    async def limit_1(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        await channel.edit(user_limit=button.label)
        await disable(self, button, inter)

    @disnake.ui.button(label="2", custom_id="limit:2", style=disnake.ButtonStyle.blurple)
    async def limit_2(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        await channel.edit(user_limit=button.label)
        await disable(self, button, inter)

    @disnake.ui.button(label="4", custom_id="limit:4", style=disnake.ButtonStyle.blurple)
    async def limit_4(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        await channel.edit(user_limit=button.label)
        await disable(self, button, inter)

    @disnake.ui.button(label="5", custom_id="limit:5", style=disnake.ButtonStyle.blurple)
    async def limit_5(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        await channel.edit(user_limit=button.label)
        await disable(self, button, inter)

    @disnake.ui.button(label="8", custom_id="limit:8", style=disnake.ButtonStyle.blurple)
    async def limit_8(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        await channel.edit(user_limit=button.label)
        await disable(self, button, inter)

    @disnake.ui.button(label="10", custom_id="limit:10", style=disnake.ButtonStyle.blurple)
    async def limit_10(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        await channel.edit(user_limit=button.label)
        await disable(self, button, inter)

    # TODO 4 5 6 10 self + -


class SelectServer(disnake.ui.Select):

    def __init__(self):
        options = [
            SelectOption(
                label="SkyWars №1",
                description="Если собираетесь тут играть",
                emoji="🟦"
            ),
            disnake.SelectOption(
                label="SkyWars №2", description="Если собираетесь тут играть", emoji="🟦"
            ),
            disnake.SelectOption(
                label="SkyWars №3", description="Если собираетесь тут играть", emoji="🟦"
            ),
            disnake.SelectOption(
                label="BedWars №1", description="123", emoji="🟥"
            ),
            disnake.SelectOption(
                label="BedWars №2", description="321", emoji="🟥"
            ),
            disnake.SelectOption(
                label="BedWars №3", description="123231", emoji="🟥"
            ),
            disnake.SelectOption(
                label="Duels №1", description="", emoji="🟪"
            ),
            disnake.SelectOption(
                label="Murder Mystery №1", description="", emoji="🟨"
            ),
            disnake.SelectOption(
                label="Murder Mystery №2", description="", emoji="🟨"
            ),
            disnake.SelectOption(
                label="Survival №1", description="Your favourite colour is green", emoji="🟩"
            )
        ]

        super().__init__(
            placeholder="Нажмите, чтобы выбрать сервер!",
            custom_id="select_server",
            max_values=1,
            row=1,
            options=options
        )

    async def callback(self, inter: disnake.MessageInteraction):
        try:
            print("1. мы тут")
            channel = await get_channel(inter.guild, inter.user.id)
            print(f"2. {channel.name}")
            name = await channel_name(self.values[0])
            print(f"3. {name}")
            await channel.edit(name=name)
            print("4. ренейм")
            embed = disnake.Embed(title=f"Название: {name}")
            print("5. всё")
            await inter.response.edit_message(embed=embed)
        except Exception as e:
            print(e)


class NameView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectServer())

    # async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
    #     channel = await get_channel(inter.guild, inter.user.id)
    #
    #     if channel is None:  # человек не создавал голосовой канал
    #         await inter.response.send_message(
    #             f"`1` Создайте голосовой, зайдя в <#{voice_create_id}>. \n"
    #             f"`2` Вам создадут и переместят вас. \n"
    #             f"`3` Только находясь в нём, вы можете использовать это!", ephemeral=True)
    #         return False
    #     elif channel is not None and inter.user.voice is not None:  # создавал и в войсе
    #
    #         if channel.id == inter.user.voice.channel.id:  # в своём войсе
    #             return True
    #
    #         else:  # не в своём войсе
    #             await inter.response.send_message(
    #                 f"Зайдите в свой голосовой канал {channel.mention}, чтобы настроить его!",
    #                 ephemeral=True)
    #             return False
    #
    #     elif channel is not None and inter.user.voice is None:  # создавал но не войсе
    #         await inter.response.send_message(
    #             f"Зайдите в свой голосовой канал {channel.mention}, чтобы настроить его!",
    #             ephemeral=True)
    #         return False

    @disnake.ui.button(label="Общение", custom_id="name:talk", style=disnake.ButtonStyle.green, row=0)
    async def talk(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        name = await channel_name(button.label)
        await channel.edit(name=name)
        await disable(self, button, inter)

    @disnake.ui.button(label="Музыка", custom_id="name:music", style=disnake.ButtonStyle.green, row=0)
    async def music(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        name = await channel_name(button.label)
        await channel.edit(name=name)
        await disable(self, button, inter)

    @disnake.ui.button(label="Оффтоп", custom_id="name:offtop", style=disnake.ButtonStyle.green, row=0)
    async def offtop(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        name = await channel_name(button.label)
        await channel.edit(name=name)
        await disable(self, button, inter)

    @disnake.ui.button(label="Ввести название", custom_id="name:custom", style=disnake.ButtonStyle.gray, row=2)
    async def custom_name(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(
            title="Личные каналы",
            custom_id="custom_name",
            components=[disnake.ui.TextInput(
                label="Изменить название",
                placeholder="Введите здесь название канала",
                custom_id="name",
                max_length=25,
            )],
        )
        try:
            modal_inter: disnake.ModalInteraction = await inter.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "custom_name" and i.author.id == inter.author.id
            )
        except TimeoutError:
            return

        name = await channel_name(modal_inter.text_values["name"])
        channel = await get_channel(inter.guild, inter.user.id)
        await channel.edit(name=name)
        embed = disnake.Embed(title=f"Название: {name}")
        await modal_inter.response.edit_message(embed=embed)


class VoiceView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        channel = await get_channel(inter.guild, inter.user.id)

        if channel is None:  # человек не создавал голосовой канал
            await inter.response.send_message(
                f"`1` Создайте голосовой, зайдя в <#{voice_create_id}>. \n"
                f"`2` Вам создадут и переместят вас. \n"
                f"`3` Только находясь в нём, вы можете использовать это!", ephemeral=True)
            return False
        elif channel is not None and inter.user.voice is not None:  # создавал и в войсе

            if channel.id == inter.user.voice.channel.id:  # в своём войсе
                return True

            else:  # не в своём войсе
                await inter.response.send_message(
                    f"Зайдите в свой голосовой канал {channel.mention}, чтобы настроить его!",
                    ephemeral=True)
                return False

        elif channel is not None and inter.user.voice is None:  # создавал но не войсе
            await inter.response.send_message(
                f"Зайдите в свой голосовой канал {channel.mention}, чтобы настроить его!",
                ephemeral=True)
            return False

    @disnake.ui.button(custom_id="voice_view:name", label="Название", style=disnake.ButtonStyle.blurple)
    async def name(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        embed = disnake.Embed(title=f"Название: {channel.name}")
        await inter.response.send_message(embed=embed, view=NameView(), ephemeral=True)

    @disnake.ui.button(custom_id="voice_view:limit", label="Размер", style=disnake.ButtonStyle.blurple)
    async def limit(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message(view=LimitView(), ephemeral=True)


class VoiceCog(commands.Cog):
    """
    Всё что связано с войсами на сервере!
    Ф: выключить NSFW, очистить чат войса, удалить и создать войс
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.views_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.views_added:
            self.bot.add_view(VoiceView())
            self.bot.add_view(NameView())
            self.bot.add_item(SelectServer())
            self.bot.views_added = True

        print(f"{self.bot.user} | {__name__}")

    @commands.command(name="гс")
    @commands.has_role(977974127304515614)
    async def voice_settings(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Управление гооловым каналом",
            description="ТУТ НАСТРОЙКИ, НАСТРАИВАТЬ НАДО"
        )
        await ctx.send(embed=embed, view=VoiceView())

    # TODO тук-тук, к вам хочет зайти @человкек

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """"Создать, удалить канал"""
        # Eсли участник зашёл/перешёл/вышел.
        # before.channel = None - зашел в гс сервера
        # after.channel = None - вышел с гс сервера

        # выключить NSFW
        if before.channel and before.channel.voice_states == {} and before.channel.is_nsfw():
            try:
                await before.channel.edit(nsfw=False, reason="Канал пустой, зачем его оставлять с матом?")
            except Exception as e:
                print(e)

        # очистить чат
        if before.channel and before.channel.voice_states == {} and before.channel.id not in custom_rooms \
                and before.channel.id != voice_create_id:
            try:
                await before.channel.purge(limit=None)
            except Exception as e:
                print(e)

        # удаляем канал
        if before.channel and before.channel.id in custom_rooms and before.channel.voice_states == {}:
            custom_rooms.pop(before.channel.id, custom_rooms[before.channel.id])
            try:
                await before.channel.delete(reason="[Собственные Каналы] Канал пуст")
            except Exception as e:
                print(e)

        if after.channel and after.channel.id == voice_create_id:
            # создаём канал
            in_cooldown = await is_cooldown(member.id)
            if in_cooldown:
                # если юзер в кулдаунде
                await after.channel.send(
                    f"{member.mention}, Исользуйте через {await cooldown_time(member.id)} сек!",
                    delete_after=15
                )
                await member.move_to(None)
            else:
                # если юзер не в кулдаунде
                emoji_list = ["👀", "💭", "✨", "🌿", "🌠", "🎆", "💞", "🚩", "🌈", "🍞", "💮", "🎲", "🤟",
                              "🌼", "🌠", "🎉", "🎂", "🎀", "🎈", "🎁", "🎶"]
                created_channel = await after.channel.guild.create_voice_channel(
                    name=f"{member.display_name} {choice(emoji_list)}",
                    reason="[Собственные Каналы] Создание",
                    category=after.channel.category,
                    position=after.channel.position + 1,
                    overwrites={member: disnake.PermissionOverwrite(view_channel=True, manage_channels=True)}
                )

                # добавляем в список канал и его создателя-участника
                custom_rooms.update({created_channel.id: member.id, member.id: created_channel.id})

                # переносим участника в его канал
                await sleep(2)
                try:
                    await member.move_to(created_channel, reason="[Cобственные Каналы] Он создал свой канал!")

                    # подсказка
                    tip_embed = disnake.Embed(
                        title=f"Напоминаем, что вы можете:",
                        description="• Выгнать непритяного пользователя! \n• Сделать канал приватным, чтобы никто не "
                                    "зашёл! "
                    )
                    await created_channel.send(embed=tip_embed)

                    # добавляем пользователю кулдаун
                    await add_cooldown(member.id, 30)

                except disnake.errors.HTTPException:
                    await created_channel.delete()

                    # добавляем пользователю кулдаун
                    await add_cooldown(member.id, 15)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(VoiceCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
