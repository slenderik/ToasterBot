#Coffe bot
import os
import typing
import disnake
from disnake.ext import commands

bot = commands.Bot(".")
bot.remove_command("help")

#materials and another things
color = 0xFFEDC6
logo_url = "https://media.discordapp.net/attachments/925973441524424716/925973463192199178/new_year_bread_2.png"


@bot.event
async def on_ready():
	print(f"{bot.user} | Панель управления")
 
 
@bot.slash_command()
@commands.is_owner()
async def cog(inter: disnake.ApplicationCommandInteraction):
	pass


@cog.sub_command()
@commands.is_owner()
async def load(
	inter: disnake.ApplicationCommandInteraction,
	extension: str
):
	bot.load_extension(f"Cogs.{extension}")
	await inter.response.send_message(f"Винтик {extension} загружен", ephemeral=True)


@cog.sub_command()
@commands.is_owner()
async def unload(
	inter: disnake.ApplicationCommandInteraction,
	extension: str
):
	bot.unload_extension(f"Cogs.{extension}")
	await inter.response.send_message(f"Винтик {extension} выгружен", ephemeral=True)


@cog.sub_command()
@commands.is_owner()
async def reload(
	inter: disnake.ApplicationCommandInteraction,
	extension: str
):
	bot.reload_extension(f"Cogs.{extension}")
	await inter.response.send_message(f"Винтик {extension} перезагружен", ephemeral=True)


@cog.sub_command()
@commands.is_owner()
async def list(
	inter: disnake.ApplicationCommandInteraction,
):
	'''Показывает список дополнений
	'''
	extension_list  = ""
	
	for filename in os.listdir("./"):
		if filename.startswith("_") and filename.endswith(".py"):
			#add to list all extension
			extension_list += f"{filename[:-3]}, \n"
	
	emb = disnake.Embed(
		title="Список дополнений",
		description=extension_list,
		colour=color,
	)
	#send list of extension
	await inter.response.send_message(embed=emb, ephemeral=True)

for filename in os.listdir("./"):
	if filename.startswith("_") and filename.endswith(".py"):
		bot.load_extension(f"{filename[:-3]}")


bot.run("ODc1MDg0MzgzMjg2MDg3Njkx.YRQX1w.DtmzpbMWMUvOpwS7U8YBkLPZr4c")
