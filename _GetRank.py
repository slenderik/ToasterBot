#get rank
import disnake
from typing import List
from requests import get
from coffe import color
from disnake.ext import commands

class GetRankCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.color = color
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.bot.user} | /получить привилегию")
	
	CHANNEL_ID = 879594073420353548
	RANK_ORIGIN = ["Куплена", "Выйграна", "Выдана"]
	 
	@commands.slash_command(name="получить")
	async def get(self, inter: disnake.ApplicationCommandInteraction):
		pass
	
	
	@get.sub_command(
		name="привелегии"
	)
	async def rank(
		self,
		inter: disnake.ApplicationCommandInteraction,
		никнейм: str,
		откуда: str,
	):
		"""Если у вас есть привелегия(-и) на сервере
			
		Parameters
		----------
		никнейм: Просто введите ваш никнейм
		откуда: Откуда привилегия? Куплена, выйграна, выдана.
		"""
		await inter.response.send_message("Ожидайте, заявка отправлена.", ephemeral=True)
		offset = 0

		def search_request(nickname):
			TOKEN = "862be8a8862be8a8862be8a83e86531f0e8862b862be8a8e731d70a4db6e27a927b37a5"
			VERSION = 5.131
			DOMAIN = "breadixdonations"
			response_ = get(
				"https://api.vk.com/method/wall.search/",
				params={
					"access_token": TOKEN,
					"v": VERSION,
					"domain": DOMAIN,
					"query": nickname,
					"offset": offset,
				}
			)
			return response_
		
		response = search_request(никнейм)
		post_count = response.json()["response"]["count"]
		
		def get_server(text):
			servers = ("bedwars", "skywars", "murder mystery", "survival")
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
			description=f"Имя пользователя: __{inter.user}__ \nИгровой никнейм: __{никнейм}__ \nОткуда: **{откуда}**",
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
		
		
	@rank.autocomplete("откуда")
	async def get_autocomp(
		self,
		inter: disnake.ApplicationCommandInteraction,
		string: str
	):
		string = string.lower()
		return [lang for lang in self.RANK_ORIGIN if string in lang.lower()]

def setup(bot):
	print(" + GetRankCog")
	bot.add_cog(GetRankCog(bot))

def teardown (bot):
	print(" – GetRankCog")