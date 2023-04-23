import os
from disnake import Embed, ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog


class RemoteCogsCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="модуль")
    @commands.is_owner()
    async def cog(self, inter: ApplicationCommandInteraction):
        pass

    cogs = []
    # add to list all extension
    for filename in os.listdir("./Cogs/"):
        if filename.endswith(".py"):
            cogs.append(f"cogs.{filename[:-3]}")

    for filename in os.listdir("./events/"):
        if filename.endswith(".py"):
            cogs.append(f"events.{filename[:-3]}")

    cogs = commands.option_enum(cogs)

    @cog.sub_command(name="список")
    @commands.is_owner()
    async def list(self, inter: ApplicationCommandInteraction):
        """Показать список дополнений"""
        extension_list = ""
        for filename in os.listdir("./Cogs/"):
            if filename.endswith(".py"):
                # add to list all extension
                extension_list += f"{filename[:-3]}, \n"
        cog_list_embed = Embed(title="Список дополнений", description=extension_list)
        await inter.response.send_message(embed=cog_list_embed, ephemeral=True)

    @cog.sub_command(name="загрузить")
    @commands.is_owner()
    async def load(self, inter: ApplicationCommandInteraction, extension: cogs):
        """"""


def setup(bot: Bot) -> None:
    bot.add_cog(RemoteCogsCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
