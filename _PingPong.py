import disnake
from disnake.ext import commands

class PingPongCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.bot.user} | .ping")

	@commands.command()
	async def ping(self, ctx: commands.Context):
		await ctx.send("pong!")
		
def setup(bot):
	print(" + PingPongCog")
	bot.add_cog(PingPongCog(bot))

def teardown (bot):
	print(" – PingPongCog")