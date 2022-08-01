import disnake
from disnake import Embed


class Confirm(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="Подтвердить", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()

    #emoji=":negative_squared_cross_mark:",
    #emoji=":white_check_mark:",

    @disnake.ui.button(label="Отказ", style=disnake.ButtonStyle.red)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("", ephemeral=True)
        self.value = False
        self.stop()


class SendToChat(disnake.ui.View):

    def __init__(self, message: disnake.ApplicationCommandInteraction):
        super().__init__(timeout=None)
        self.message = message

    @disnake.ui.button(custom_id="send_to_chat", label="Отправить в чат?", style=disnake.ButtonStyle.gray, row=1)
    async def send_to_chat(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = Embed(
            title="Вы уверены что хотите отправить это в чат?",
            description="Все в чате смогут увидеть это сообщение. Подтверждайте только если уверены что это сообщение "
                        "кому-то нужно в чате. "
        )
        view = Confirm()
        await inter.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
        if view.value is None:
            print("Timed out...")
            await inter.response.edit_message(embed=Embed(title="Время вышло"))
            # raise SendErrror(
        elif view.value:
            print("Confirmed...")
            await inter.channel.send(await self.message.original_message())
        else:
            print("Cancelled...")
            await inter.response.edit_message(embed=Embed(title="Отказ"))
