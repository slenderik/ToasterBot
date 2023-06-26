import os

from disnake import Embed, ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog, ExtensionAlreadyLoaded, NoEntryPointError, ExtensionFailed, ExtensionNotFound


class CogRemote(Cog):

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
        cog_list_embed = Embed(title="Модули:", description=extension_list)
        await inter.response.send_message(embed=cog_list_embed, ephemeral=True)

    @cog.sub_command(name="загрузить")
    @commands.is_owner()
    async def cog_load(self, inter: ApplicationCommandInteraction, extension: cogs):
        """Загрузить дополнение"""
        print(f"[{__name__}] {inter.user.name}: загружает {extension}")
        try:
            self.bot.load_extension(extension)

        except ExtensionNotFound:
            print(f"ERROR IN [{__name__}] {inter.user.name}: {extension} не найден.")
            await inter.send(f"**Ошибка** `{extension}` не найден.", ephemeral=True)
        except ExtensionAlreadyLoaded:
            print(f"ERROR IN [{__name__}] {inter.user.name}: {extension} уже загружен.")
            await inter.send(f"**Ошибка** `{extension}` уже загружен. Для начала выгрузите его или перезагрузите.", ephemeral=True)
        except NoEntryPointError:
            print(f"ERROR IN [{__name__}] {inter.user.name}: В {extension} нет setup()!")
            await inter.send(f"**Ошибка** В `{extension}` нет setup() функции.", ephemeral=True)
        except ExtensionFailed:
            print(f"ERROR IN [{__name__}] {inter.user.name}: Ошибка в {extension}!")
            await inter.send(f"**Ошибка** Ошибка в `{extension}` при загрузке.", ephemeral=True)

        else:
            await inter.response.send_message(f"✔ {extension} загружен!", ephemeral=True)

    @cog.sub_command(name="выгрузить")
    @commands.is_owner()
    async def cog_unload(self, inter: ApplicationCommandInteraction, extension: cogs):
        """Выгрузить дополнение"""
        print(f"[{inter.user.name}]: выгружает {extension}")
        self.bot.unload_extension(extension)
        cog_unload_embed = Embed(title=f"Дополнение {extension} выгружено!")
        await inter.response.send_message(embed=cog_unload_embed, ephemeral=True)

    @cog.sub_command(name="перезагрузить")
    @commands.is_owner()
    async def cog_reload(self, inter: ApplicationCommandInteraction, extension: cogs):
        """Загрузить дополнение"""
        print(f"[{inter.user.name}]: перезагружает {extension}")
        self.bot.reload_extension(extension)
        cog_reload_embed = Embed(title=f"Дополнение {extension} перезагружено!")
        await inter.response.send_message(embed=cog_reload_embed, ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(CogRemote(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
