from time import time
import disnake
from random import choice
from asyncio import sleep
from disnake.utils import get
from disnake.ext import commands

# тук-тук
# к вам хочет зайти @человке

chat_id = 823820166478823464
voice_create_id = 879387831385088020
server_id = 823820166478823462
logo_url = "https://media.discordapp.net/attachments/925973441524424716/925973455919251536/logo_bread.png?width=473&height=473"


# inter.bot self.bot
# inter.user member
async def get_channel_by_id(bot, user) -> object:
    """Вернуть канала автора."""
    server = bot.get_guild(server_id)
    owner_channel = custom_rooms[user.id]
    channel = get(server.voice_channels, id=owner_channel)
    return channel


async def disable(self, button, inter):
    """Отключить нажатую кнопку."""
    #включаем все кнопки в том же ряду
    for child in self.children:
        if isinstance(child, disnake.ui.Button):
            if child.row == button.row:
                child.disabled = False
    # Выключаем нажатую кнопку
    button.disabled = True
    await inter.response.edit_message(view=self)


custom_rooms = {}


async def channel_name(name):
    """Вернуть название канала с учётом разных штук."""
    print(f"1. {name}")
    if "🔞" in name:
        print(name)
        name = f"[🔞] {name}"
    print(f"2. {name}")
    return name

class VoiceView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Общение",
        style=disnake.ButtonStyle.green,
        custom_id="voice_view:talk",
        row=0
    )
    async def talk(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        name = await channel_name(button.label)
        await channel.edit(name=name, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="Музыка",
        style=disnake.ButtonStyle.green,
        custom_id="voice_view:music",
        row=0
    )
    async def music(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        name = await channel_name(button.label)
        await channel.edit(name=name, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="Оффтоп",
        style=disnake.ButtonStyle.green,
        custom_id="voice_view:offtop",
        row=0
    )
    async def offtop(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        name = await channel_name(button.label)
        await channel.edit(name=name, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="SkyWars",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:skywars",
        row=1
    )
    async def skywars(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        name = await channel_name(button.label)
        await channel.edit(name=name, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="BedWars",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:blurple",
        row=1
    )
    async def bedwars(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        name = await channel_name(button.label)
        await channel.edit(name=name, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="Survival",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:survival",
        row=1
    )
    async def survival(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        name = await channel_name(button.label)
        await channel.edit(name=name, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="MurderMustery",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:murdermustery",
        row=1
    )
    async def murdermustery(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        name = await channel_name(button.label)
        await channel.edit(name=name, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="С матом",
        emoji="🔞",
        style=disnake.ButtonStyle.red,
        custom_id="voice_view:yes_profanity",
        row=2
    )
    async def yes_profanity(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        await channel.edit(name=f"[🔞] {channel.name}", reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="Без мата",
        style=disnake.ButtonStyle.red,
        custom_id="voice_view:no_profanity",
        row=2
    )
    async def no_profanity(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        await channel.edit(name=channel.name[4:], nsfw=True, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="Открыть",
        emoji="🔓",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:unlock_channel",
        row=3
    )
    async def unlock_channel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        channel = await get_channel(inter.bot, inter.user)
        user = inter.user
        overwrites = {user: disnake.PermissionOverwrite(view_channel=True, manage_channels=True)}
        await channel.edit(overwrites=overwrites, reason="[Собственные Каналы] панель управления")
        await disable(self, button, inter)

    @disnake.ui.button(
        label="Закрыть",
        emoji="🔒",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:lock_channel",
        row=3
    )
    async def lock_channel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(
        label="2",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:user_limit_two",
        row=4
    )
    async def user_limit_two(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(
        label="4",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:user_limit_four",
        row=4
    )
    async def user_limit_four(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(
        label="5",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:user_limit_five",
        row=4
    )
    async def user_limit_five(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(
        label="6",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:user_limit_six",
        row=4
    )
    async def user_limit_six(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)

    @disnake.ui.button(
        label="10",
        style=disnake.ButtonStyle.blurple,
        custom_id="voice_view:user_limit_ten",
        row=4
    )
    async def user_limit_ten(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await disable(self, button, inter)


cooldowns = {}


async def cooldown_time(member_id) -> str:
    """"Вернуть время на кулдаун."""
    if cooldowns.get(member_id) is not None:
        cooldown_time = str(cooldowns[member_id] - round(time()))
        return cooldown_time
    else:
        cooldown_time = "0 UwU"
        return cooldown_time


async def is_cooldown(member_id) -> bool:
    """"Вернуть значение, находится ли пользователь в кулдауне."""
    if cooldowns.get(member_id) is not None:
        return True
    else:
        return False


async def add_cooldown(member_id):
    """Добавить в кулдауны время когда участник сможет использовать команду снова."""
    cooldown = round(time())
    cooldown += 30  #время отката/кулдауна
    cooldown_time = {member_id: cooldown}
    cooldowns.update(cooldown_time)
    await sleep(30)
    cooldowns.pop(member_id)


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

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """"Создать, удалить канал и панель управления"""
        #Eсли участник зашёл/перешёл/вышел.
        #before.channel = None - зашел в гс сервера
        #after.channel = None - вышел с гс сервера

        print(member.name)
        print(before.channel)
        print(after.channel)

        if before.channel != None and before.channel.id in custom_rooms and before.channel.voice_states == {}:
            channel_id = before.channel.id
            owner_id = custom_rooms[before.channel.id]
            server = self.bot.get_guild(server_id)
            owner_user = await server.fetch_member(owner_id)

            #удаляем панель управления из ЛС
            x = f"{before.channel.id}-1"
            print(f"id: {x}")
            message_id = custom_rooms.get(x)
            print(message_id)
            if message_id != None:
                user_dm = await owner_user.create_dm()
                message = await user_dm.fetch_message(message_id)
                await message.delete()


            #пишем создателю о удалении
            await send_to_dm(
                user=owner_user,
                guild=before.channel.guild,
                text="Ваш канал удалён",
                deleting=15
            )
            #удаляем канал
            print('1')
            custom_rooms.pop(owner_id, message_id);
            print('2')
            custom_rooms.pop(channel_id)
            print('3')
            await before.channel.delete(reason="[Собственные Каналы] Канал пуст")
            print('4')


        if after.channel != None and after.channel.id == voice_create_id:
            in_cooldown = await is_cooldown(member.id)
            if in_cooldown:
                #если юзер в кулдаунде
                await send_to_dm(
                    guild=after.channel.guild,
                    user=member,
                    text=f"Исользуйте команду через {await cooldown_time(member.id)} сек.",
                    deleting=15
                )
            else:
                #создаём канал
                emoji_list = ["👀", "💭", "✨", "🌿", "🌠", "🎆", "💞", "🚩", "🌈", "🍞", "💮", "🎲", "🤟",
                              "🌼", "🌠", "🎉", "🎂", "🎀", "🎈", "🎁", "🎶"]
                overwrites = {member: disnake.PermissionOverwrite(view_channel=True, manage_channels=True)}

                created_channel = await after.channel.guild.create_voice_channel(
                    name=f"{member.display_name}{choice(emoji_list)}",
                    reason="[Собственные Каналы] Создание",
                    category=after.channel.category,
                    position=after.channel.position + 1,
                    overwrites=overwrites
                )

                #добавляем в список канал и его создателя-участника
                new_channel = {created_channel.id: member.id, member.id: created_channel.id}
                custom_rooms.update(new_channel)

                #переносим участника в его канал
                await sleep(2)
                await member.move_to(created_channel, reason="[Cобственные Каналы] Он создал свой канал!")

                #отправляем панель управления пользователю
                control_panel_embed = disnake.Embed(
                    title=f"<:Breadix:940540206866628641> | Панель управления",
                    description=f"""Вы создали канал, название: `{created_channel.name}`
                                    Помните, что вы можете:
                                    * Закрыть канал (Никто не сможет зайти) `/приват-канал закрыть`
                                      * Открыть канал для опред. человека `/приват-канал разрешить-для [человек]`
                                      * Открыть канал, все кроме запрещёёных смогут зайти `/приват-канал открытьф`
                                    * Выкинуть и запретить заходить к вам (остальные смогнут) `/приват-канал выкинуть [человек]`
                                """
                )
                #control_panel_embed.set_thumbnail(url=logo_url)
                control_panel_embed.set_footer(text="Вот некоторые настройки:")

                try:
                    dm_member = await member.create_dm()
                    control_panel_message = await dm_member.send(embed=control_panel_embed, view=VoiceView())
                    control_message = {f"{created_channel.id}-1": control_panel_message.id}
                    custom_rooms.update(control_message)
                except:
                    await send_instruction(guild=after.channel.guild, user=member)

                await add_cooldown(member.id)


def setup(bot):
    bot.add_cog(VoiceCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
