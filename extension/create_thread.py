import disnake
from disnake import SelectOption, Embed


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
            select_values = self.options
            for value in select_values:
                value.default = True
                await inter.response.edit_messsage(f"{self.values[0]}", view=self.view)
        except Exception as e:
            print(e)
            await inter.response.send_message(f"Что-то пошло ни так! {e}")


class ThreadView(disnake.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TimeSelect())

    @disnake.ui.button(emoji=":information_source:", custom_id="thread:info")
    async def info_thread(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        thread_info_embed = Embed(
            title="Информация",
            description=""
        )
        await inter.response.edit_message(ephemeral=True)


async def create_thread(message: disnake.Message, time: int = 4320, slowmode: int = None):
    thread = await message.create_thread(name="", auto_archive_duration=time, slowmode_delay=slowmode)
    await thread.send(":gear: **Настройки ветки**", view=ThreadView())


class ThreadCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.thread_view_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.information_views_added:
            self.add_view(ThreadView())
            self.thread_view_added = True

        print(f"{self.bot.user} | {__name__}")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ThreadCog(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
