# выключить NSFW, очистить чат войса, удалить и создать войс, отключить из афк
from asyncio import sleep
from random import choice

import disnake
from disnake.utils import get
from disnake.ext import commands
from disnake import SelectOption, Embed
from disnake.ui import Button, Select
from utils.config import afk_channel_id

custom_rooms = {}


async def get_channel(guild: object, user_id: int) -> object | None:
    """Вернуть канал автора."""
    return get(guild.voice_channels, id=custom_rooms[user_id]) if custom_rooms.get(user_id, None) is not None else None


# кулдауны
cooldowns = {}
cooldown_create = {}
cooldown_name = {}
voice_create_id = 1031152112236761140


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
        options = [
            SelectOption(label="SkyWars №1", description="Если собираетесь тут играть", emoji="🟦"),
            SelectOption(label="SkyWars №2", description="Если собираетесь тут играть", emoji="🟦"),
            SelectOption(label="SkyWars №3", description="Если собираетесь тут играть", emoji="🟦"),
            SelectOption(label="BedWars №1", emoji="🟥"),
            SelectOption(label="BedWars №2", emoji="🟥"),
            SelectOption(label="BedWars №3", emoji="🟥"),
            SelectOption(label="Duels №1", emoji="🟪"),
            SelectOption(label="Murder Mystery №1", emoji="🟨"),
            SelectOption(label="Murder Mystery №2", emoji="🟨"),
            SelectOption(label="Survival №1", emoji="🟩")
        ]
        components = [
            Button(label="Общение", custom_id="voice_name_talk"),
            Button(label="Музыка", custom_id="voice_name_music"),
            Button(label="Оффтоп", custom_id="voice_name_offtop"),
            Select(placeholder="Нажмите, чтобы выбрать сервер!", max_values=1, row=1, options=options,
                   custom_id="voice_name_server"),
            Button(label="Ввести название", custom_id="voice_name_custom_name"),
        ]
        await inter.response.send_message(embed=embed, components=components, ephemeral=True)

    @disnake.ui.button(custom_id="voice_view:limit", label="Лимит", style=disnake.ButtonStyle.blurple)
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
            self.bot.views_added = True

        print(f"{self.bot.user} | {__name__}")

    @commands.command(name="гс")
    async def voice_settings(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Управление личным каналом!",
            description="У нас есть каналы. Они каналы."
                        "[ **Название** ] канала. Спасибо что используйте! \n"
                        "[ **Лимит** ] участников в канале. Не выкидывает участников.\n"
        ).set_footer(text="Нажмите на кнопки ниже, чтобы настроить канал!")
        await ctx.send(embed=embed, view=VoiceView())

    # TODO тук-тук, к вам хочет зайти @человкек

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceChannel,
                                    after: disnake.VoiceChannel):
        """"Создать, удалить канал"""
        # Если участник зашёл/перешёл/вышел.
        # before.channel = None - зашел в гс сервера
        # after.channel = None - вышел с гс сервера

        # выключить NSFW
        if before.channel and before.channel.voice_states == {} and before.channel.is_nsfw():
            try:
                await before.channel.edit(nsfw=False, reason="Канал пустой, зачем его оставлять с матом?")
            except Exception as e:
                print(f"{__name__} Error: {e}")

        # очистить чат
        if before.channel and before.channel.voice_states == {} and before.channel.id not in custom_rooms \
                and before.channel.id != voice_create_id:
            try:
                await before.channel.purge(limit=None)
            except Exception as e:
                print(f"{__name__} Error: {e}")

        # отключить отошедших
        if after.channel is not None and after.channel.id == afk_channel_id:
            await after.channel.send("Эй, похоже вы немного отошли? Надеемся с вами всё хорошо ^^ Мы вас отключим от "
                                     "этого канала через пару минут.")
            await sleep(300)
            try:
                await member.move_to(None)
            except Exception as e:
                print(f"{__name__} Error: {e}")

        # удаляем канал
        if before.channel and before.channel.id in custom_rooms and before.channel.voice_states == {}:
            custom_rooms.pop(before.channel.id, custom_rooms[before.channel.id])
            try:
                await before.channel.delete(reason="[Собственные Каналы] Канал пуст")
                return
            except Exception as e:
                print(f"{__name__} Error: {e}")

        # создаём канал
        if after.channel and after.channel.id == voice_create_id:
            # если юзер в кулдаунде
            if is_cooldown(member.id, cooldown_create):
                cooldown = await cooldown_time(member.id, cooldown_create)
                await after.channel.send(
                    f"{member.mention}, Используйте через {cooldown} сек!",
                    delete_after=cooldown
                )
                # выкинуть из войса
                await member.move_to(None)
                return

            # если юзер не в кулдаунде
            emoji_list = ["👀", "💭", "✨", "🌿", "🌠", "🎆", "💞", "🚩", "🌈", "🍞", "💮", "🎲", "🤟",
                          "🌼", "🌠", "🎉", "🎂", "🎀", "🎈", "🎁", "🎶"]
            overwrites = {member: disnake.PermissionOverwrite(view_channel=True, manage_channels=True)}

            created_channel = await after.channel.guild.create_voice_channel(
                name=f"{member.display_name} {choice(emoji_list)}",
                reason="[Собственные Каналы] Создание",
                category=after.channel.category,
                position=after.channel.position + 1,
                overwrites=overwrites
            )
            # добавляем в список канал и его создателя-участника
            custom_rooms.update({created_channel.id: member.id, member.id: created_channel.id})
            # переносим участника в его канал
            await sleep(1)

            try:
                await member.move_to(created_channel, reason="[Личные Каналы] Он создал свой канал!")
                # подсказка
                tip_embed = disnake.Embed(
                    title=f"Напоминаем, что вы можете:",
                    description="• Выгнать непритяного пользователя! \n• Сделать канал приватным, чтобы никто не "
                                "зашёл! "
                )
                await created_channel.send(embed=tip_embed)
                # добавляем пользователю кулдаун
                await add_cooldown(member.id, cooldown_create, 30)  # при успешном переносе в канал

            except disnake.errors.HTTPException:
                await created_channel.delete()
                # добавляем пользователю кулдаун
                await add_cooldown(member.id, cooldown_create, 15)  # при ошибке переноса

    @commands.Cog.listener("on_button_click")
    async def voices_buttons_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id and inter.component.custom_id.startswith("voice_name"):
            if inter.component.custom_id == "voice_name_talk":

                # если юзер в кулдаунде
                if is_cooldown(member.id, cooldown_name):
                    cooldown = await cooldown_time(member.id, cooldown_name)
                    embed = Embed(
                        title="Извените, но..",
                        description=f"Вы можете в ручную настроить название канала."
                                    f"Бот сможет это через {cooldown} сек!"
                    ).set_footer(text="Это ограничение Discord (API)"),
                    await inter.response.send_message(embed=embed, ephemeral=True)
                    return

                # если юзер не в кулдаунде
                button = inter.component
                channel = await get_channel(inter.guild, inter.user.id)
                name = button.label
                await channel.edit(name=name)
                embed = disnake.Embed(title=f"Название: {name}")
                await inter.response.edit_message(embed=embed)

        elif inter.component.custom_id and not inter.component.custom_id.startswith("limit"):
            pass

    @commands.Cog.listener("on_dropdown")
    async def voices_select_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id and inter.component.custom_id.startswith("voice_name"):
            try:
                channel = await get_channel(inter.guild, inter.user.id)
                name = inter.values[0]
                await channel.edit(name=name)
                embed = disnake.Embed(title=f"Название: {name}")
                await inter.response.edit_message(embed=embed)

            except Exception as e:
                print(f"{__name__} Error: {e}")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(VoiceCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
