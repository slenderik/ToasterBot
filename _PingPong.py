import disnake
from disnake.ext import commands

class PingPongCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.bot.user} | {__name__}")

	@commands.command(name="пинг", aliases=["ping"])
	async def ping(self, ctx: commands.Context):
		ping_embed = disnake.Embed(
			title=f"Пинг: {round(self.bot.latency, 3)} сек!"
		)
		await ctx.send(embed=ping_embed)
		
def setup(bot):
	bot.add_cog(PingPongCog(bot))
	print(f" + {__name__}")

def teardown(bot):
	print(f" – {__name__}")