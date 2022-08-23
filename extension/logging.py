from disnake import Embed

guild_id = 610142528271810560
log_channel_id = 988330342391873587


async def log_send(bot, embed: Embed):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(log_channel_id)
    await channel.send(embed=embed)
