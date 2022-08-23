from disnake import Embed

guild_id = 823820166478823462
log_channel_id = 857298133943451678 #TEST


async def log_send(bot, embed: Embed):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(log_channel_id)
    await channel.send(embed=embed)
