from disnake import ApplicationCommandInteraction, Embed
from disnake.ext import commands
from disnake.ext.commands import is_owner
from utils.checks import discord_admins


class CommandsList(commands.Cog):
    """Показывает команды бота"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="команды")
    async def commands_list(self, inter: ApplicationCommandInteraction):
        """
        Показывает все команды и их использование
        """
        text = ""
        for command in self.bot.global_slash_commands:
            local_command = self.bot.get_slash_command(command.name)

            check = local_command.checks
            print("CHECKS: ")
            print(check)
            [print(i) for i in check]
            print(is_owner in check)
            print(discord_admins() in check)

            text += f"</{command.name}:{command.id}> \n"

            print(f"</{command.name}:{command.id}> \n")

        embed = Embed(title=f"Команды", description=text)

        await inter.send(embed=embed)

    @commands.slash_command(name="команды2", guild_ids=[823820166478823462])
    async def commands_list2(self, inter: ApplicationCommandInteraction):
        """Показывает все команды и их использование"""

        embed = Embed(title=f"Команды")

        for cog in self.bot.cogs:
            if not isinstance(cog, commands.Cog):
                cog = self.bot.get_cog(cog)

            if cog is None:
                RuntimeError

            text = ""

            for command in cog.get_commands():
                local_command = self.bot.get_slash_command(command.name)

                check = command.checks

                print("CHECKS: ")
                print(check)
                [print(i) for i in check]
                print(is_owner in check)
                print(discord_admins(inter) in check)
                print(f"</{command.name}:{command}> \n")

                text += f"</{command.name}:{command}> \n"

            for slash_command in cog.get_slash_commands():
                api_slash_command = self.bot.get_global_command_named(name=slash_command.name)

                if slash_command.parents:
                    print(slash_command.parents)
                if api_slash_command is not None:
                    text += f"</{slash_command.name}:{api_slash_command.id}> \n"
                else:
                    text += f"{slash_command.name} \n"

            embed.add_field(name=cog.qualified_name, value=cog.description + '\n' + text, inline=False  )

        await inter.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CommandsList(bot))
    print(f" + {__name__}")


def teardown(bot: commands.Bot) -> None:
    print(f" – {__name__}")
