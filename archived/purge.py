from disnake import ApplicationCommandInteraction, Forbidden, Member, NotFound, HTTPException, Embed, TextChannel
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog

#from utils.config import audit_log_channel_id


class PurgeCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="очистить")
    @commands.has_role(1074308897315246170)
    async def purge(self, inter: ApplicationCommandInteraction, count: int, member: Member = None):
        """
        Удалить сообщения

        #TODO удаление от участника или по времени.
        """
        if not isinstance(inter.channel, TextChannel):
            await inter.response.send_message(f"Работает только в текстовом канале.")

        deleted = 0
        problems = 0

        async for message in inter.channel.history():
            try:
                for attachment in message.attachments:

                    channel = self.bot.fetch_channel(audit_log_channel_id)
                    file = await attachment.to_file(
                        description=f"Удалённое фото от пользователя {message.author.name}"
                                    f"{message.author.discriminator} ({message.author.id})"
                    )
                    await channel.send(file=file)

                await message.delete()

            except Forbidden:
                problems += 1
                await inter.response.send_message(f"Ошибка: нет прав просмотра истории или управление сообщениями.")
            except NotFound:
                problems += 1
                await inter.response.send_message(f"Ошибка: сообщение не найдено или уже удалено.")
            except HTTPException:
                problems += 1
                await inter.response.send_message(f"Ошибка: ошибка удаления сообщения.")

            else:
                deleted += 1

        embed = Embed(
            title=f"Удалено {deleted} сообщений",
            description=f"Ошибок: {problems}"
        )

        await inter.response.send_message(embed=embed, ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(PurgeCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
