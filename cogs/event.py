import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog


class EventsCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="event")
    async def event(self, inter: ApplicationCommandInteraction):
        pass

    @event.sub_command(name="mute-all")
    async def event_mute(self, inter: ApplicationCommandInteraction, channel: disnake.VoiceChannel):
        """Получить задержку работы бота."""
        for member in channel.members:
            try:
                await member.edit(mute=True)
            except Exception as e:
                print(f"Event: {e}")

        await inter.response.send_message(f"Все в {channel.mention} замучены!")

    @event.sub_command(name="unmute-all")
    async def event_unmute(self, inter: ApplicationCommandInteraction, channel: disnake.VoiceChannel):
        """Получить задержку работы бота."""
        for member in channel.members:
            try:
                await member.edit(mute=False)
            except Exception as e:
                print(f"Event: {e}")

        await inter.response.send_message(f"Все в {channel.mention} размучены!")


def setup(bot: Bot) -> None:
    bot.add_cog(EventsCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
