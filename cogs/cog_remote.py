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

    @commands.slash_command(name="дополнение")
    @commands.is_owner()
    async def cog(self, inter: ApplicationCommandInteraction):
        pass

    cogs = []
    for filename in os.listdir("./Cogs/"):
        if filename.endswith(".py"):
            # add to list all extension
            cogs.append(f"cogs.{filename[:-3]}")

    for filename in os.listdir("./events/"):
        if filename.endswith(".py"):
            # add to list all extension
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
        """Загрузить дополнение"""
        self.bot.load_extension(extension)
        cog_load_embed = Embed(title=f"Дополнение {extension} загружено!")
        await inter.response.send_message(embed=cog_load_embed, ephemeral=True)

    @cog.sub_command(name="выгрузить")
    @commands.is_owner()
    async def unload(self, inter: ApplicationCommandInteraction, extension: cogs):
        """Выгрузить дополнение"""
        self.bot.unload_extension(extension)
        cog_unload_embed = Embed(title=f"Дополнение {extension} выгружено!")
        await inter.response.send_message(embed=cog_unload_embed, ephemeral=True)

    @cog.sub_command(name="перезагрузить")
    @commands.is_owner()
    async def creload(self, inter: ApplicationCommandInteraction, extension: cogs):
        """Загрузить дополнение"""
        self.bot.reload_extension(extension)
        cog_reload_embed = Embed(title=f"Дополнение {extension} перезагружено!")
        await inter.response.send_message(embed=cog_reload_embed, ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(RemoteCogsCog(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
