import disnake
from coffe import color, logo_url
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
		"""Показывает магазин, в котором вы можете потратить валюту."""
		store = disnake.Embed(
			title="Магазин",
			description="Все доступные товары за валюту <:breadcoin:858583099096956938>\nИспользуйте ``!купить-товар <название>`` в <#710692543255281725>\n[!] Для товара с ``+`` используйте ``!купить-товар VIPplus``",
			colour=self.color,
		)
		store.set_thumbnail(url=self.logo_url)
		
		mini_games_items = disnake.Embed(
			title="Привелегии на мини-играх",
			description="Покупая товар, ты получаешь купленную тобой привилегию на одном из серверов мини-игр на твой выбор. Со всеми возможностями привилегий можно ознакомиться на [сайте магазина](https://shop.breadixpe.ru/).",
			colour=self.color,
		)
		mini_games_items.add_field(
			name="MVP - 1.590.000 <:breadcoin:858583099096956938>",
			value="Базовая привилегия мини-играх SkyWars, BedWars и Murder Mystery!",
		)
		mini_games_items.add_field(
			name="VIP - 790.000 <:breadcoin:858583099096956938>",
			value="Самая доступная привилегия на Sky Wars, BedWars и Murder Mystery!",
		)
		mini_games_items.set_footer(text="shop.breadixpe.ru", icon_url=self.logo_url)
		
		survival_products = disnake.Embed(
			title="Привилегии на Survival",
			description="Покупая товар, ты получаешь купленную тобой привилегию на сервере Survival. Со всеми возможностями привилегий можно ознакомиться на [сайте магазина](https://shop.breadixpe.ru/).",
			colour=self.color,
		)
		survival_products.add_field(
			name="VIP+ - 2.590.000 <:breadcoin:858583099096956938>",
			value="Самая популярная привилегия на Survival!",
		)
		survival_products.add_field(
			name="VIP - 1.190.000 <:breadcoin:858583099096956938>",
			value="Популярная привилегия на Survival!",
		)
		survival_products.add_field(
			name="Creative - 990.000 <:breadcoin:858583099096956938>",
			value="Базовая привилегия на Survival!",
		)
		survival_products.add_field(
			name="Fly - 290.000 <:breadcoin:858583099096956938>",
			value="Самая доступная привилегия на Survival!",
		)
		survival_products.set_footer(text="shop.breadixpe.ru", icon_url=self.logo_url)
		
		other_goods = disnake.Embed(
			title="Прочее",
			description="Покупая товар, ты получаешь возоможность создать приватное место для себя и своих друзей.О других особенностях кланов можно ознакомться в <#610742443847057408>.",
			colour=self.color,
		)
		other_goods.add_field(
			name="Кланы - 15.000 <:breadcoin:858583099096956938>",
			value="Самое лучшее и крутое что вы можете купить"
		)
		
		store_embeds = [store, mini_games_items, survival_products, other_goods]
		
		await inter.response.send_message(embeds=store_embeds, ephemeral=True)
		

def setup(bot):
	print(" + Магазин")
	bot.add_cog(StoreCog(bot))

def teardown (bot):
	print(" – Магазин")
