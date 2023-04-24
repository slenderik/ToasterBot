from datetime import datetime
from disnake.ext import commands, tasks
from mcstatus import BedrockServer

from os import environ
from utils.config import get_data_config
from utils.config import SERVERS_PORTS, status_voice_channel_id, status_message_id, status_text_channel_id
from disnake import Embed, Forbidden, HTTPException


async def update_voice_status(bot):
    try:
        server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=19132))
        voice_channel = await bot.fetch_channel(status_voice_channel_id)
        await voice_channel.edit(name=f"Онлайн — {server.players_online}")

    except TimeoutError:
        voice_channel = await bot.fetch_channel(status_voice_channel_id)
        await voice_channel.edit(name="❤️ Похоже, сервер выключен!")


async def update_status_message(bot):
    server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=19132))
    embed = Embed(
        title=f"Онлайн: {server.players_online}",
        color=0xf9f9f9,
        timestamp=datetime.now()
    )
    embed.set_image(url="https://i.ibb.co/cQcs6XT/max-res.gif")
    embed.set_footer(icon_url='https://i.ibb.co/kSqg89s/logo16x16-3.png', text='Обновлено')

    server_emojis = {
        4108: '<:sw1:1077962812996993064>',
        5732: '<:sw2:1077962839517573192>',
        6360: '<:bw1:1077962902289518673>',
        4248: '<:bw2:1077962930739499171>',
        1313: '<:bw3:1077962956601561171>',
        9624: '<:mm1:1077962982807584860>',
        7198: '<:mm2:1077963008107622492>',
        59898: '<:surv:1059520290461339778>',
        7219: '<:duels:1059520345775800391>',
    }

    server_emojis = {
        4108: '<:sw1:1077962812996993064>',
        5732: '<:sw2:1077962839517573192>',
        6360: '<:bw1:1077962902289518673>',
        4248: '<:bw2:1077962930739499171>',
        1313: '<:bw3:1077962956601561171>',
        9624: '<:mm1:1077962982807584860>',
        7198: '<:mm2:1077963008107622492>',
        59898: '<:surv:1059520290461339778>',
        7219: '<:duels:1059520345775800391>',
    }

    server_emojis = {
        "sw1": '<:sw1:1077962812996993064>',
        "sw2": '<:sw2:1077962839517573192>',
        "bw1": '<:bw1:1077962902289518673>',
        "bw2": '<:bw2:1077962930739499171>',
        "bw3": '<:bw3:1077962956601561171>',
        "mm1": '<:mm1:1077962982807584860>',
        "mm2": '<:mm2:1077963008107622492>',
        "surv": '<:surv:1059520290461339778>',
        "duels": '<:duels:1059520345775800391>',
    }

    games_modes_names = "sw1" "sw2" "bw1" "bw2" "bw3" "mm1" "mm2" "surv" "duels"

    server_ports_murder_mystery = "9624, 7198"
    server_ports_bedwars = "6360, 4248, 1313"
    server_ports_skywars = "4108, 5732"
    server_ports_survival = "59898"
    server_ports_duels = "7219"

    games_modes_names = "sw1" "sw2" "bw1" "bw2" "bw3" "mm1" "mm2" "surv" "duels"
    for game_mode_name in games_modes_names:
        ports = environ.get("server_ports_" + game_mode_name)
        text = ""
        for port in ports.split(", "):
            try:
                server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=port))
                text += f"{server_emojis[port]} **{server.players_online}**︲"
            except TimeoutError:
                return "Сервер выключен!"

    # добавляем поля серверов в ебмед
    games_modes_names = "skywars, bedwars, duels, survival, murder_mystery"
    for game_mode_name in games_modes_names:
        ports = environ.get("server_ports_" + game_mode_name)
        text = ""
        for port in ports.split(", "):
            server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=port))
            text += f"{server_emojis[port]} **{server.players_online}**︲"

    # добавляем поля серверов в ебмед
    for server_name, ports in SERVERS_PORTS.items():
        text = ""
        for port in ports:
            server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=port))
            text += f"{server_emojis[port]} **{server.players_online}**︲"

        embed.add_field(name=f"{server_name}", value=f"{text[:-1]}", inline=True)


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
        return ctx.author.id in [377383169420427264, 324922480642752512] # slenderik and golosovy discord id

    @commands.command(aliases=["статус"])
    @commands.check(is_owners)
    async def status(self, ctx: commands.Context, *, text):
        await ctx.message.delete()
        await ctx.send(f"[ <t:{round(datetime.now().timestamp())}:R> ] {text}")


def setup(bot):
    bot.add_cog(StatusCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
