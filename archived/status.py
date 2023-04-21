from datetime import datetime
from disnake.ext import commands, tasks
from mcstatus import BedrockServer

from utils.config import SERVERS_PORTS, status_voice_channel_id, server_emojis, status_message_id, \
    status_text_channel_id
from utils.logging import send_to_admin, send_to_logs
from disnake import Embed, Forbidden, HTTPException


async def update_voice_status(bot):
    try:
        voice_channel = await bot.fetch_channel(status_voice_channel_id)
        server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=19132))
        await voice_channel.edit(name=f"Онлайн — {server.players_online}")

    except Forbidden as e:
        embed = Embed(
            title=f"Forbidden {__name__}!",
            description=f"У меня нет прав изменить канал <#{status_voice_channel_id}>! {e}"
        )
        await send_to_admin(bot=bot, embed=embed)

    except HTTPException as e:
        embed = Embed(
            title=f"HTTPException {__name__}!",
            description=f"Ошибка изменения канала: {e}"
        )
        await send_to_admin(bot=bot, embed=embed)

    except TypeError as e:
        embed = Embed(
            title=f"TypeError {__name__}!",
            description=f"Информация о разрешении на перезапись находится не в надлежащей форме: {e}"
        )
        await send_to_admin(bot=bot, embed=embed)

    except Exception as e:
        embed = Embed(
            title=f"Exception {__name__}!",
            description=f"Ошибка: {e}"
        )
        await send_to_admin(bot=bot, embed=embed)


async def update_status_message(bot):
    # создаём ембед
    server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=19132))
    embed = Embed(
        title=f"Онлайн: {server.players_online}",
        color=0xf9f9f9,
        timestamp=datetime.now()
    )
    embed.set_image(url="https://i.ibb.co/cQcs6XT/max-res.gif")
    embed.set_footer(icon_url='https://i.ibb.co/kSqg89s/logo16x16-3.png', text='Обновлено')

    # добавляем поля серверов в ебмед
    for server_name, ports in SERVERS_PORTS.items():
        text = ""
        for port in ports:
            server = await BedrockServer.async_status(BedrockServer(host="play.breadixpe.ru", port=port))
            text += f"{server_emojis[port]} **{server.players_online}**︲"

        embed.add_field(name=f"{server_name}", value=f"{text[:-1]}", inline=True)

    try:
        channel = await bot.fetch_channel(status_text_channel_id)
        message = await channel.fetch_message(status_message_id)
        await message.edit(embed=embed)

    except Exception as e:
        channel = await bot.fetch_channel(status_text_channel_id)
        await channel.send(embed=embed)

        embed = Embed(
            title=f"Exception {__name__}!",
            description=f"Ошибка: {e}"
        )
        await send_to_logs(bot=bot, embed=embed)


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

    async def is_owner(ctx):
        return ctx.author.id == 316026178463072268

    @commands.command(aliases=["статус"])
    @commands.check(is_owner)
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
