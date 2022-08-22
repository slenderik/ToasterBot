import disnake
from disnake import SelectOption


class TimeSelect(disnake.ui.Select):

    def __init__(self):
        options = [
            SelectOption(label="1 Час", description="Ветка будет заархивирована после 1 часа без активности",
                         value=60),
            SelectOption(label="1 День", description="Ветка будет заархивирована после 1 дня без активности",
                         value=1440),
            SelectOption(label="3 Дня", description="Ветка будет заархивирована после 3 дней без активности",
                         value=4320, default=True),
            SelectOption(label="1 Недели", description="Ветка будет заархивирована после 1 часа без активности",
                         value=10080)
        ]
        super().__init__(
            placeholder="Нажмите чтобы выбрать роль гендера",
            max_values=1,
            options=options,
            custom_id="thread:time"
        )

    async def callback(self, inter: disnake.MessageInteraction):
        try:
            await inter.channel.edit(archived=self.values[0])
        except Exception as e:
            print(e)
            await inter.response.send_message(f"Что-то пошло ни так! {e}")


class ThreadView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TimeSelect())

    @disnake.ui.button(emoji=":information_source:", style=disnake.ButtonStyle.blurple, custom_id="thread:info")
    async def notifications(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.original_message_edit(view=None, ephemeral=True)


async def create_thread(message: disnake.Message, time: int = 4320, slowmode: int = None):
    thread = await message.create_thread(auto_archive_duration=time, slowmode_delay=slowmode)
    await thread.send(":gear: **Настройки ветки**", view=ThreadView())
