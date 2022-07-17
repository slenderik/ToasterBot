from asyncio import sleep, TimeoutError
from random import choice
from time import time

import disnake
from disnake.ext import commands
from disnake.utils import get

# тук-тук
# к вам хочет зайти @человке

voice_create_id = 879387831385088020
server_id = 823820166478823462
logo_url = "https://media.discordapp.net/attachments/925973441524424716/925973455919251536/logo_bread.png?width=473" \
           "&height=473 "

custom_rooms = {}


async def is_owner(user_id: int) -> bool:
    """Вернуть значение владелец ли человек"""
    return custom_rooms.get(user_id, None) is not None


async def in_channel(user: object) -> bool:
    """Вернуть значение ползователь в канале?"""
    return user.voice is not None


async def in_owned_channel(user: object, channel: object) -> bool:
    """Вернуть значение пользователь в своём канале?"""
    return user.voice.channel.id == channel.id


async def channel_name(name: str) -> str:
    """Вернуть название канала с учётом разных штук."""
    if "🔞" in name:
        name = f"[🔞] {name}"
    return name


async def get_channel(guild: object, user_id: int) -> object | None:
    """Вернуть канал автора."""
    if custom_rooms.get(user_id, None) is not None:
        return get(guild.voice_channels, id=custom_rooms[user_id])
    else:
        return None


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
    if cooldowns.get(user_id) is not None:
        cooldown = str(cooldowns[member_id] - round(time()))
    else:
        cooldown = "0 UwU"
    return cooldown


async def is_cooldown(user_id: int) -> bool:
    """"Вернуть значение, находится ли пользователь в кулдауне."""
    if cooldowns.get(user_id) is not None:
        return True
    else:
        return False


async def add_cooldown(user_id: int):
    """Добавить в кулдауны время когда участник сможет использовать команду снова."""
    cooldown: int = round(time())
    cooldown += 30  # время отката/кулдауна
    cooldown = {user_id: cooldown}
    cooldowns.update(cooldown)
    await sleep(30)
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

    @disnake.ui.button(custom_id="voice_view:user_limit_two", label="2", style=disnake.ButtonStyle.blurple, row=4)
    async def user_limit_two(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(custom_id="voice_view:user_limit_four", label="4", style=disnake.ButtonStyle.blurple, row=4)
    async def user_limit_four(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(custom_id="voice_view:user_limit_five", label="5", style=disnake.ButtonStyle.blurple, row=4)
    async def user_limit_five(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(custom_id="voice_view:user_limit_six", label="6", style=disnake.ButtonStyle.blurple, row=4)
    async def user_limit_six(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(custom_id="voice_view:user_limit_ten", label="10", style=disnake.ButtonStyle.blurple, row=4)
    async def user_limit_ten(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)


class NameView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        owner = await is_owner(inter.user.id)
        in_voice = await in_channel(inter.user)

        if owner and in_voice:
            channel = await get_channel(inter.guild, inter.user.id)
            if channel is not None:
                in_owned = await in_owned_channel(inter.user, channel)
                if in_owned:
                    return True
            else:
                await inter.response.send_message(
                    f"Вы должны находится в своём голосовом канале, чтобы настроить его",
                    ephemeral=True)
                return False
        elif owner and not in_voice:
            await inter.response.send_message(f"Вы должны зайти в голосовой канал.", ephemeral=True)
            return False
        elif not owner:
            await inter.response.send_message(f"Вы должны создать голосовой канал.", ephemeral=True)
            return False
        """
        Вы должны создать свой голосовой канал, зайдя в <#879387831385088020>
        И уже находясь в нём, вы сможете  использовать эту прелестную кнопкушку.
        """

    @disnake.ui.button(label="Общение", style=disnake.ButtonStyle.green, row=0)
    async def talk(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        name = await channel_name(button.label)
        await channel.edit(name=name)
        await disable(self, button, inter)

    @disnake.ui.button(label="Музыка", style=disnake.ButtonStyle.green, row=0)
    async def music(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        name = await channel_name(button.label)
        await channel.edit(name=name)
        await disable(self, button, inter)

    @disnake.ui.button(label="Оффтоп", style=disnake.ButtonStyle.green, row=0)
    async def offtop(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        name = await channel_name(button.label)
        await channel.edit(name=name)
        await disable(self, button, inter)

    # sw bw surv duels
    @disnake.ui.button(custom_id="name:skywars", label="SkyWars", style=disnake.ButtonStyle.blurple, row=1)
    async def skywars(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.guild, inter.user.id)
        name = await channel_name(button.label)
        await channel.edit(name=name)
        await disable(self, button, inter)
        await inter.response.send_message(view=LimitView())

    @disnake.ui.button(label="Ввести название", style=disnake.ButtonStyle.gray, row=2)
    async def custom_name(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(
            title="Вести собственное название",
            custom_id="voice:name",
            components=[disnake.ui.TextInput(
                label="Название",
                placeholder="Введите здесь название канала",
                custom_id="name:custom_name",
                max_length=50,
            )],
        )
        try:
            modal_inter: disnake.ModalInteraction = await inter.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "voice:name" and i.author.id == inter.author.id,
                timeout=300
            )
        except TimeoutError:
            return

        name = await channel_name(modal_inter.text_values["name:custom_name"])
        channel = await get_channel(inter.guild, inter.user.id)
        await channel.edit(name=name)
        await modal_inter.response.defer()


class VoiceView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(custom_id="voice_view:name", label="Общение", style=disnake.ButtonStyle.green)
    async def name(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message(view=NameView(), ephemeral=True)

    @disnake.ui.button(custom_id="voice_view:limit", label="Колличество участников", style=disnake.ButtonStyle.green)
    async def limit(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message(view=LimitView(), ephemeral=True)


class VoiceCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_views_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.voice_views_added:
            self.bot.add_view(VoiceView())
            self.bot.voice_views_added = True

        print(f"{self.bot.user} | {__name__}")

    @commands.command(name="гс")
    @commands.has_role(977974127304515614)
    async def voice_settings(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Управление гооловым каналом",
            description="ТУТ НАСТРОЙКИ, НАСТРАИВАТЬ НАДО"
        )
        await ctx.send(embed=embed, view=VoiceView())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """"Создать, удалить канал"""
        # Eсли участник зашёл/перешёл/вышел.
        # before.channel = None - зашел в гс сервера
        # after.channel = None - вышел с гс сервера
        if before.channel is not None and before.channel.id in custom_rooms and before.channel.voice_states == {}:
            # удаляем канал
            custom_rooms.pop(before.channel.id, custom_rooms[before.channel.id])
            await before.channel.delete(reason="[Собственные Каналы] Канал пуст")

        if after.channel is not None and after.channel.id == voice_create_id:
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
                await member.move_to(created_channel, reason="[Cобственные Каналы] Он создал свой канал!")

                # подсказка
                tip_embed = disnake.Embed(
                    title=f"Напоминаем, что вы можете:",
                    description="• Выгнать непритяного пользователя! \n• Сделать канал приватным, чтобы никто не зашёл!"
                )
                await created_channel.send(embed=tip_embed)

                # добавляем пользователю кулдаун
                await add_cooldown(member.id)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(VoiceCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
