#get rank
import disnake
from requests import get
from coffe import color
from disnake.ext import commands

class GetRankCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.color = color
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.bot.user} | /получить роли")
	
	@commands.command()
	async def скрин(self, ctx: commands.Context):
		guide_emb = disnake.Embed(
			title="Как мне получить роль?",
			description="1. Зайдите на сервер.\n2. Авторизуйтесь в аккаунт и **отойдите от спавна.**\n3. Сделайте скриншот сообщения о входе.\n4. Отправьте изображение суда.",
			 color=self.color
		)
		await ctx.send(embed=guide_emb)
	
	CHANNEL_ID = 879594073420353548
	
	@commands.slash_command(name="получить")
	async def get(self, inter: disnake.ApplicationCommandInteraction):
		pass
	
	
	@get.sub_command(name="роли")
	async def roles(
		self,
		inter: disnake.ApplicationCommandInteraction,
		никнейм: str,
	):
		"""Если у вас есть привелегия(-и) на сервере
			
		Parameters
		----------
		никнейм: Просто введите ваш никнейм
		"""
		await inter.response.send_message("Ожидайте, заявка отправлена.", ephemeral=True)
		
		offset = 0

		def search_request(nickname):
			TOKEN = "25991c5d25991c5d25991c5d6d25e1ebfb2259925991c5d447917c5be90392810a81ccd"
			VERSION = "5.131"
			DOMAIN = "breadixdonations"
			OWNER_ID = "-151687251"
			response_ = get(
				"https://api.vk.com/method/wall.search/",
				params={
					"access_token": TOKEN,
					"owner_id": OWNER_ID,
					"v": VERSION,
					"domain": DOMAIN,
					"query": nickname,
					"owners_only": "1",
					"offset": offset,
				}
			)
			return response_
		
		response = search_request(никнейм)
		post_count = response.json()["response"]["count"]
		
		def get_server(text):
			servers = ("bedwars", "skywars", "murder mystery", "murdermystery" "survival")
			numbers = ("№1", "№2", "№3")
			
			server_output = {
				"bedwars": "BW",
				"skywars": "SW",
				"murder mystery": "MM",
				"survival": "surv",
			}
			
			for server in servers:
				if int(text.find(server)) != -1:
					for number in numbers:
						if text.find(number)!= -1:
							server = f"{server_output[server]}{number[1:]}"
							return server
		
		
		def get_purchase(text):
			purchases = ("fly", "vip+", "vip", "mvp++", "mvp+", "mvp", "creative+", "creative", "разбан", "1000 монет", "5000 монет", "10000 монет")
			
			for purchase in purchases:	
				if int(text.find(purchase)) != -1:
					return purchase
		
		def get_nickname(text):
			text = text[6:]
			index = int(text.find("купил"))
			if index != -1:
				nickname = text[:index-1]
				return nickname
			index = int(text.find("приобрел"))
			if index != -1:
				nickname = text[:index-1]
				return nickname
		
		posts = ""
		if post_count != 0:
			
			for post in range(post_count):
				
				response = search_request(никнейм)
				from_id = str(response.json()["response"]["items"][0]["from_id"])
				if str(from_id) == "-151687251":	
				
					owner_id = str(response.json()["response"]["items"][0]["owner_id"])
					url_id = str(response.json()["response"]["items"][0]["id"])
					post_url = "https://vk.com/wall" + owner_id + "_" + url_id
					
					text = response.json()["response"]["items"][0]["text"]
					
					offset +=1
					text = text.lower()
					posts += f"{post+1}. [{get_nickname(text)} | {get_server(text)} | {get_purchase(text)}]({post_url})\n"
				else:
					post_count -= 1
		
		admin_embed = disnake.Embed(
			title=":scroll: Заявка на привелегии",
			description=f"Имя: __{inter.user}__ \nНикнейм: __{никнейм}__",
			color = self.color,
		)
		if posts != "":
			admin_embed.add_field(
				name=f":mag: Поиск во ВКонтакте({post_count}):",
				value=f">>> {posts}",
			)
		
		if post_count == 0:			
			admin_embed.add_field(
				name=":mag: Поиск во ВКонтакте:",
				value="`Ничего не найдено`",
			)
		
		admin_channel = self.bot.get_channel(self.CHANNEL_ID)
		
		await admin_channel.send(
			f"{inter.user.mention} | {никнейм}",
			embed=admin_embed
		)


def setup(bot):
	bot.add_cog(GetRankCog(bot))
	print(f" + {__name__}")

def teardown (bot):
	print(f" – {__name__}")
