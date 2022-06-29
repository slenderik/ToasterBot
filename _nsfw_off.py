# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands


class VoiceNsfwOffCog(commands.Cog):
    """Выключить настройку NSFW после выхода ввсех участников из не удаляемого канала."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel.voice_states == {} and before.channel.is_nsfw():
            try:
                await before.channel.edit(nsfw=False, reason="Канал пустой, зачем ему оставаться с матом?")
            except Exception as e:
                print(e)


def setup(bot):
    bot.add_cog(VoiceNsfwOffCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
