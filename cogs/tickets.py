import datetime
import time

import disnake
from disnake import SelectOption
from disnake.ext import commands
from disnake.ui import TextInput, Select

tickets_category_id = 940666384734646292


async def ticket_count(category) -> int:
    """Вернуть номер тикета"""
    n = category.text_channels
    if not n:
        return 1
    n = str(n[len(n) - 1])
    if n[1:2] == "︱":
        n = int(n[:1])
        n += 1
    else:
        n = int(n[:2])
        n += 1
    return n


class TicketModal(disnake.ui.Modal):
    def __init__(self, target_user=None) -> None:
        self.target_user = target_user

        components = [
            TextInput(
                label="Никнейм",
                placeholder="Ведите ваш игровой никнейм",
                custom_id="Никнейм",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            Select(
                placeholder="Нажмите, чтобы выбрать с чем это связано",
                min_values=1,
                max_values=1,
                options=[
                    SelectOption(
                        label="Discord",
                        description="Всё что связано с сооществом в Discord",
                        emoji="<:Discord:999582738640277544>",
                        value="1",
                    ),
                    SelectOption(
                        label="Игрвые сервера",
                        description="Всё что связано с игровыми серверами",
                        emoji="🎮",
                        value="2",
                    ),
                    SelectOption(
                        label="Другое",
                        description="но всё равно связано с проектом BreadixWorld.",
                        value="3",
                    ),
                ]
            ),
            Select(
                placeholder="Нажмите, чтобы выбрать категорию обращения",
                min_values=1,
                max_values=1,
                options=[
                    SelectOption(
                        label="Жалоба",
                        description="На читера или пользователя."
                    ),
                    SelectOption(
                        label="Получить роли привилегий",
                        description="Если у вас есть привилегии на сервере.",
                    ),
                    SelectOption(
                        label="Обратная связь",
                        description="Поделитесь вашим мнением. Что понравилось, что нет, что хотели видеть по-другому"
                    ),
                    SelectOption(
                        label="Апелляция",
                        description="Апелляция на разбан."
                    ),
                ]
            ),
            TextInput(
                label="Опишите причину",
                placeholder="Предложение, жалоба, вопрос, заявка на роли. \nВы сможете ОТПРАВИТЬ ФОТО и добавить",
                custom_id="Причина",
                style=disnake.TextInputStyle.paragraph,
                min_length=5,
                required=False,
                max_length=1024,
            ),

        ]
        super().__init__(title="Создать обращение", custom_id="create_ticket", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        user = inter.user

        category = inter.bot.get_channel(tickets_category_id)
        permission = {
            user: disnake.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True,
                                              read_message_history=True)
        }

        embed = disnake.Embed(title="Обращение!")
        for key, value in inter.text_values.items():
            print(key, value)
            if not (key and value):
                continue
            embed.add_field(name=key, value=value, inline=False)

        if self.target_user is not None:
            if self.target_user.bot:
                await inter.response.send_message(
                    f"ЭЙ, {user.mention}, {self.target_user.mention} это бот!",
                    ephemeral=True
                )
                return

            creator_user = inter.user
            channel = await category.create_text_channel(
                name=f"{await ticket_count(category)}︱{user.display_name}",
                overwrites=permission,
                topic=f":penguin: **Информация**"
                      f"\nСоздан: **{creator_user.name}** ({creator_user.id})"
                      f"\nДля: **{user.name}** ({user.id}) "
                      f"\nВремя: <t:{round(time.mktime(datetime.datetime.now().timetuple()))}:R>",
                reason=f"{creator_user.name}({creator_user.id})"
            )
            await channel.send(f"Hey, {target_user.mention}, для тебя создал тикет {user.mention}!", embed=embed)

        else:
            channel = await category.create_text_channel(
                name=f"{await ticket_count(category)}︱{user.display_name}",
                overwrites=permission,
                topic=f":penguin: **Информация** "
                      f"\nСоздан: **{user.name}** ({user.id})"
                      f"\nВремя: <t:{round(time.mktime(datetime.datetime.now().timetuple()))}:R>",
                reason=f"{user.name}({user.id})"
            )
            await channel.send(f"Hey, {user.mention}", embed=embed)

        await inter.response.send_message(
            embed=disnake.Embed(
                title="🎫 Билетик создан",
                description=f"Для: {user.mention} ({user.id}) \nКанал: {channel.mention}"),
            ephemeral=True
        )

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        await inter.response.send_message(f"Что-то пошло ни так. Ошибка: {error}", ephemeral=True)


class TicketsCog(commands.Cog):
    """Дополнение обращений"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")


    @commands.message_command(name="Создать билетик")
    @disnake.ext.commands.has_role(977974127304515614)
    async def ticket(self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
        """Создать канал обращения"""
        modal = TicketModal(target_user=message.author)
        await inter.response.send_modal(modal=modal)

    # @ticket.error
    # async def tickets(self, inter: disnake.ApplicationCommandInteraction, error):
    #     if isinstance(error, commands.MissingRole):


def setup(bot):
    bot.add_cog(TicketsCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
