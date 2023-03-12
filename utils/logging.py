from disnake import Embed
from utils.config import log_channel_id, guild_id


async def log_send(bot, embed: Embed):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(log_channel_id)

    try:
        await channel.send(embed=embed)

    except Exception as e:
        print(f"{__name__} Error: {e}")


async def send_to_admin(bot, embed: Embed):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(log_channel_id)

    try:
        await channel.send(embed=embed)

    except Exception as e:
        print(f"{__name__} Error: {e}")
