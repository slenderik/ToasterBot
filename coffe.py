#Coffe bot GitHub-версия
import os
import typing
import disnake
from disnake.ext import commands

bot = commands.Bot(".")
bot.remove_command("help")

#materials and another things
disnake.Embed.set_default_color(283593)
logo_url = "https://media.discordapp.net/attachments/925973441524424716/925973455919251536/logo_bread.png"
admin_server_id = [823820166478823462]

@bot.event
async def on_ready():
	print(f"{bot.user} • Главная")
 
 
@bot.slash_command(guild_ids=admin_server_id, name="дополнение")
@commands.is_owner()
async def cog(inter: disnake.ApplicationCommandInteraction):
	pass


@cog.sub_command(name="загрузить")
@commands.is_owner()
async def load(
	inter: disnake.ApplicationCommandInteraction,
	extension: str
):
	"""Загрузить дополнение"""
	bot.load_extension(extension)
	cog_load_embed = disnake.Embed(title=f"Дополнение {extension} загружено!")
	await inter.response.send_message(embed=cog_load_embed, ephemeral=True)


@cog.sub_command(name="выгрузить")
@commands.is_owner()
async def unload(
	inter: disnake.ApplicationCommandInteraction,
	extension: str
):
	"""Выгрузить дополнение"""
	bot.unload_extension(extension)
	cog_unload_embed = disnake.Embed(title=f"Дополнение {extension} выгружено!")
	await inter.response.send_message(embed=cog_unload_embed, ephemeral=True)


@cog.sub_command(name="перезагрузить")
@commands.is_owner()
async def reload(
	inter: disnake.ApplicationCommandInteraction,
	extension: str
):
	"""Загрузить дополнение"""
	bot.reload_extension(extension)
	cog_reload_embed = disnake.Embed(title=f"Дополнение {extension} перезагружено!")
	await inter.response.send_message(embed=cog_reload_embed, ephemeral=True)


@cog.sub_command(name="список")
@commands.is_owner()
async def list(
	inter: disnake.ApplicationCommandInteraction,
):
	"""Показать список дополнений"""
	extension_list  = ""
	for filename in os.listdir("./"):
		if filename.startswith("_") and filename.endswith(".py"):
			#add to list all extension
			extension_list += f"{filename[:-3]}, \n"
	cog_list_embed = disnake.Embed(
		title="Список дополнений",
		description=extension_list,
	)
	await inter.response.send_message(embed=cog_list_embed, ephemeral=True)


for filename in os.listdir("./"):
	if filename.startswith("_") and filename.endswith(".py"):
		bot.load_extension(f"{filename[:-3]}")


bot.run("ODc1MDg0MzgzMjg2MDg3Njkx.YRQX1w.DtmzpbMWMUvOpwS7U8YBkLPZr4c")