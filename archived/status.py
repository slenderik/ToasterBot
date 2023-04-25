from datetime import datetime
from disnake.ext import commands, tasks
from mcstatus import BedrockServer

from utils.config import get
from utils.config import status_voice_channel_id, status_message_id, status_text_channel_id
from disnake import Embed


async def update_voice_status(bot):
    try:
        server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=19132))
        voice_channel = await bot.fetch_channel(status_voice_channel_id)
        await voice_channel.edit(name=f"Онлайн — {server.players_online}")

    except TimeoutError:
        voice_channel = await bot.fetch_channel(status_voice_channel_id)
        await voice_channel.edit(name="❤️ Похоже, сервер выключен")


async def update_status_message(bot):
    server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=19132))
    embed = Embed(
        title=f"Онлайн: {server.players_online}",
        color=0xf9f9f9,
        timestamp=datetime.now()
    )
    embed.set_image(url="https://i.ibb.co/cQcs6XT/max-res.gif")
    embed.set_footer(icon_url='https://i.ibb.co/kSqg89s/logo16x16-3.png', text='Обновлено')

    emoji_4108 = "<:sw1:1077962812996993064>"
    emoji_5732 = '<:sw2:1077962839517573192>',
    emoji_6360 = '<:bw1:1077962902289518673>',
    emoji_4248 = '<:bw2:1077962930739499171>',
    emoji_1313 = '<:bw3:1077962956601561171>',
    emoji_9624 = '<:mm1:1077962982807584860>',
    emoji_7198 = '<:mm2:1077963008107622492>',
    emoji_59898 = '<:surv:1059520290461339778>',
    emoji_7219 = '<:duels:1059520345775800391>',

    ports_murder_mystery = "9624, 7198"
    ports_bedwars = "6360, 4248, 1313"
    ports_skywars = "4108, 5732"
    ports_survival = "59898"
    ports_duels = "7219"

    games_modes_names = "skywars, bedwars, duels, survival, murder_mystery"
    for game_mode_name in games_modes_names:
        ports = await get("server_ports_" + game_mode_name)
        text = ""
        for port in ports.split(", "):
            try:
                server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=int(port)))
                emoji = await get("emoji_" + port)
                text += f"{emoji} **{server.players_online}**︲"
            except TimeoutError:
                emoji = await get("emoji_" + port)
                text += f"{emoji} 🚫"

    channel = await bot.fetch_channel(status_text_channel_id)
    message = await channel.fetch_message(status_message_id)
    await message.edit(embed=embed)


class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    @tasks.loop(minutes=5)
    async def update_status(self):
        await update_voice_status(self.bot)
        await update_status_message(self.bot)

    @update_status.before_loop
    async def before_printer(self):
        print(f"[{__name__}] Ready")
        await self.bot.wait_until_ready()

    async def is_owners(ctx):
        return ctx.author.id in [377383169420427264, 324922480642752512]    # slenderik and golosovy discord id

    @commands.command(aliases=["status", "статус"])
    @commands.check(is_owners)
    async def status(self, ctx: commands.Context, *, text):
        await ctx.message.delete()
        await ctx.send(f"[ <t:{round(datetime.now().timestamp())}:R> ] {text}")


def setup(bot):
    bot.add_cog(StatusCog(bot))
    print(f" + {__name__}")


def teardown():
    print(f" – {__name__}")
