from disnake import Embed
from disnake.ext.commands import Bot
from utils.config import admin_channel_id, audit_log_channel_id


async def send_to_admin(bot: Bot, embed: Embed, embeds: list[Embed] = None):
    try:
        channel = bot.fetch_channel(admin_channel_id)
        await channel.send(embed=embed, embeds=embeds)

    except Exception as e:
        print(f"{__name__} Error: {e}")


async def send_to_logs(bot: Bot, embed: Embed, embeds: list[Embed] = None):
    try:
        channel = bot.fetch_channel(audit_log_channel_id)
        await channel.send(embed=embed, embeds=embeds)

    except Exception as e:
        print(f"{__name__} Error: {e}")
