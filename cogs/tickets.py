from disnake import ApplicationCommandInteraction, Message, DMChannel, Thread
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog


class ModMail(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not isinstance(message.channel, DMChannel):
            return

        modmail_forum_id = 1118969274527133808
        modmail_forum: Thread
        modmail_forum = self.bot.get_channel(modmail_forum_id)
        user = message.author

        if modmail_forum is None:
            return

        thread = None
        for mod_thread in modmail_forum.threads:
            print("name: ", mod_thread.name)
            print("name: ", str(user.id) in mod_thread.name)
            print("actived?: ", not mod_thread.archived)
            print("Good one?: ", str(user.id) in mod_thread.name and not mod_thread.archived)

            if (str(user.id) in mod_thread.name) and (not mod_thread.archived):
                thread = mod_thread
                print(thread)
                break

        print(thread)
        print("Create new: ", thread is not None)

        if thread is None:
            thread, message = await modmail_forum.create_thread(name=f"{user.name} ({user.id})", content=message.content)
            print(thread.name)

        files = []

        for attachment in message.attachments:
            files += await attachment.to_file(description=f"From {user.name} ({user.id})")

        await thread.send(
            content=message.content,
            embeds=message.embeds,
            files=files,
            stickers=message.stickers,
            components=message.components
        )



    @commands.slash_command()
    async def ping(self, inter: ApplicationCommandInteraction):
        """Получить задержку работы бота."""
        await inter.response.send_message(f"Задержка: {round(self.bot.latency * 1000)}мл.")


def setup(bot: Bot) -> None:
    bot.add_cog(ModMail(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
