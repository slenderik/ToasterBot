import disnake
from toaster import color, logo_url
from disnake.ext import commands

class StoreCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.color = color
		self.logo_url = logo_url
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.bot.user} | /магазин")
	
	@commands.slash_command(name="магазин")
	async def store(
		self,
		inter: disnake.ApplicationCommandInteraction,
	):
		"""Посмотрите магазин:)"""
		
		print("The Stor cmd is invoke")
		
		emb1 = disnake.Embed(
			title="Магазин",
			description="Все доступные товары, которые можно приобрести за валюту <:breadcoin:858583099096956938>\n``!купить-товар <название>`` - команда для покупки товара. Вводить в #боты :nexclamation: - при покупке товара с + вводить plus.\nПример: ``!купить-товар VIPplus``",
			colour=self.color,
		)
		emb1.set_thumbnail(url=self.logo_url)
		
		emb2 = disnake.Embed(
			title="Привелегии на мини-играх",
			description="Покупая товар, ты получаешь купленную тобой привилегию на одном из серверов мини-игр на твой выбор. Со всеми возможностями привилегий можно ознакомиться [на сайте магазина.](https://shop.breadixpe.ru/)",
			colour=self.color,
		)
		emb2.add_field(
			name="MVP - 1.590.000 <:breadcoin:858583099096956938>",
			value="Базовая привилегия мини-играх Sky Vars, BedWars и Murder Mystery!",
		)
		emb2.add_field(
			name="VIP - 790.000 <:breadcoin:858583099096956938>",
			value="Самая доступная привилегия на Sky Wars, BedWars и Murder Mystery!",
		)
		emb2.set_footer(text="shop.breadixpe.ru", icon_url=self.logo_url)
		
		emb3 = disnake.Embed(
			title="Привилегии на Survival",
			description="Покупая товар, ты получаешь купленную тобой привилегию на сервере Survival. Со всеми возможностями привилегий можно ознакомиться [на сайте магазина.](https://shop.breadixpe.ru/)",
			colour=self.color,
		)
		emb3.add_field(
			name="VIP+ - 2.590.000 <:breadcoin:858583099096956938>",
			value="Самая популярная привилегия на Survival",
		)
		emb3.add_field(
			name="VIP - 1.190.000 <:breadcoin:858583099096956938>",
			value="Популярная привилегия на Survival",
		)
		emb3.add_field(
			name="Creative - 990.000 <:breadcoin:858583099096956938>",
			value="Базовая привилегия на Survival",
		)
		emb3.add_field(
			name="Fly - 290.000 <:breadcoin:858583099096956938>",
			value="Самая доступная привилегия на Survival",
		)
		emb3.set_footer(text="shop.breadixpe.ru", icon_url=self.logo_url)
		
		
		embeds = [emb1, emb2, emb3]
		
		await inter.response.send_message(embeds=embeds, ephemeral=True)
		

def setup(bot):
	print(" + StoreCog")
	bot.add_cog(StoreCog(bot))

def teardown (bot):
	print(" – StoreCog")