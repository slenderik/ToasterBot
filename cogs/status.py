from datetime import datetime
from disnake.ext import commands
from mcstatus import

voice_channel_id = 1066055695914520606
text_channel_id = 1078357675622023228


async def update_voice_online(bot):
    try:
        voice_channel = await bot.fetch_channel(voice_channel_id)

        from mcstatus import BedrockServer

        # You can pass the same address you'd enter into the address field in minecraft into the 'lookup' function
        # If you know the host and port, you may skip this and use BedrockServer("example.org", 19132)
        server = BedrockServer.lookup("example.org:19132")

        # 'status' is the only feature that is supported by Bedrock at this time.
        # In this case status includes players_online, latency, motd, map, gamemode, and players_max. (ex: status.gamemode)
        status = server.status()
        print(f"The server has {status.players.online} players online and replied in {status.latency} ms")

        await
    except:
        ...

class StatusCog(commands.Cog):
    """Команда статуса"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.command(aliases=["статус"])
    async def status(self, ctx: commands.Context, *, text):
        """Отправить сообщение о проблемах."""
        await ctx.message.delete()
        allow_users = [377383169420427264, 324922480642752512]
        if ctx.author.id in allow_users:
            await ctx.send(f"[ <t:{round(datetime.now().timestamp())}:R> ] {text}")


def setup(bot):
    bot.add_cog(StatusCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
