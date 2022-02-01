import aiohttp
import asyncio
import disnake
from disnake.ext import commands

class AiohttpsCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.bot.user} | .aiohttps test")

	@commands.slash_command(guild_ids=[823820166478823462])
	async def test(self, inter: disnake.ApplicationCommandInteraction):
		
		offset = 0
		
		async def search_request(search_nickname):
			"""Вернуть информацию поиска  по никнейму, в группе с донатами."""
			TOKEN = "25991c5d25991c5d25991c5d6d25e1ebfb2259925991c5d447917c5be90392810a81ccd"
			VERSION = "5.131"
			GROUP_NAME = "breadixdonations"
			GROUP_NAME = "-151687251"
			async with aiohttp.ClientSession() as session:
				async with session.get(f"https://api.vk.com/method/wall.search?access_token={TOKEN}&v={VERSION}&domain={GROUP_NAME}&owner_id={GROUP_NAME}&query={search_nickname}&owners_only=1&offset={offset}") as r:
					if r.status == 200:
						js = await r.json()
						print(js)
						return js
		
		async def url(response) -> str:
			"""Вернуть ссылку на пост ВКонтакте."""
			owner_id = str(response["response"]["items"][0]["owner_id"])
			url_id = str(response["response"]["items"][0]["id"])
			url = "https://vk.com/wall" + owner_id + "_" + url_id
			return url
			
		никнеймы = ["swali", "slenderik", "swali"]
		
		for никнейм in никнеймы:
			response = await search_request(никнейм)
			print(response)
			post_count = response["response"]["count"]
			print(post_count)
			
			posts = ""
			for post in range(post_count):
				response = await search_request(никнейм)
				text = response["response"]["items"][0]["text"]
				
				posts += f"{await url(response)}\n"
				offset +=1
			await asyncio.sleep(3)
		
		await inter.response.send_message(f"{posts}", ephemeral=True)


def setup(bot):
	bot.add_cog(AiohttpsCog(bot))
	print(f" + {__name__}")

def teardown (bot):
	print(f" – {__name__}")