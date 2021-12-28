#Gender buttons
from coffe import color
from disnake.ext import commands
from disnake.utils import get
from disnake import ButtonStyle
import disnake


class GenderView(disnake.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
	
	#Измените id здесь, если они изменились
	bio_role_id = 916368041405722645
	man_role_id = 844279863959748659
	girl_role_id = 844279699257294888
	another_role_id = 916173998151307354
	
	
	async def delete_roles(self, inter: disnake.MessageInteraction):
		man_role = get(inter.guild.roles, id=self.man_role_id)
		girl_role = get(inter.guild.roles, id=self.girl_role_id)
		another_role = get(inter.guild.roles, id=self.another_role_id)
		
		roles_list = (man_role, girl_role, another_role)
		
		for role in roles_list: 
			if role in inter.user.roles:
				await inter.user.remove_roles(role)
	
	@disnake.ui.button(
		label="Девочка",
		style=ButtonStyle.red,
		custom_id="gender:girl"
	)
	async def girl(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		await self.delete_roles(inter=inter)
		bio_role = get(inter.guild.roles, id=self.bio_role_id)
		girl_role = get(inter.guild.roles, id=self.girl_role_id)
		await inter.user.add_roles(bio_role, girl_role)
		await inter.response.send_message("Гендер: девочка", ephemeral=True)
	
	
	@disnake.ui.button(
		label="Мальчик",
		style=ButtonStyle.blurple,
		custom_id="gender:man"
	)
	async def man(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		await self.delete_roles(inter=inter)
		bio_role = get(inter.guild.roles, id=self.bio_role_id)
		man_role = get(inter.guild.roles, id=self.man_role_id)
		await inter.user.add_roles(bio_role, man_role)
		await inter.response.send_message("Гендер: мальчик", ephemeral=True)
	
	
	@disnake.ui.button(
		label="Другое",
		style=ButtonStyle.green,
		custom_id="gender:another"
	)
	async def another(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		await self.delete_roles(inter=inter)
		bio_role = get(inter.guild.roles, id=self.bio_role_id)
		another_role = get(inter.guild.roles, id=self.another_role_id)
		await inter.user.add_roles(bio_role, another_role)
		await inter.response.send_message("Другой гендер", ephemeral=True)
	
	
class GenderCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.gender_views_added = False
		self.bot = bot
		self.color = color
	
	@commands.Cog.listener()
	async def on_ready(self):
		super().__init__()
		if not self.gender_views_added:
			self.bot.add_view(GenderView())
			self.bot.gender_views_added = True
		print(f"{self.bot.user} | .gender")
	
	
	@commands.command()
	@commands.is_owner()
	async def gender(self, ctx: commands.Context):
		emb = disnake.Embed(
			title="Нажмите на кнопки, чтобы добавить отметки в профиле.",
			colour=self.color,
		)
		emb.set_image(url="https://media.discordapp.net/attachments/916934320466309170/920321546881478656/IMG_20211214_202850.jpg")
		await ctx.send(embed=emb, view=GenderView())


def setup(bot):
	print(" + GenderCog")
	bot.add_cog(GenderCog(bot))

def teardown (bot):
	print(" – GenderCog")