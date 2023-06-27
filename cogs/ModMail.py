from disnake import ApplicationCommandInteraction, Message, DMChannel, Thread, NotFound, HTTPException
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog

modmail_forum_id: int = 1118969274527133808


class ModMail(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener("on_message")
    async def dm_forum(self, message: Message):
        # DM -> FORUM
        # пропускаем рекурсию
        if message.author.id == self.bot.user.id:
            return

        if isinstance(message.channel, DMChannel):
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
                thread, message = await modmail_forum.create_thread(
                    name=f"{user.name} ({user.id})",
                    content=message.content
                )
                print(thread.name)

            files = []

            for attachment in message.attachments:
                files += await attachment.to_file(description=f"From {user.name} ({user.id})")
            try:
                await thread.send(
                    content=message.content,
                    embeds=message.embeds,
                    files=files,
                    stickers=message.stickers,
                    components=message.components
                )
            except Exception as e:
                await message.add_reaction("⚠️")
                await thread.send(f"ERROR: `{e}`")

            else:
                await message.add_reaction("✔️")

    @commands.Cog.listener("on_message")
    async def forum_to_dm(self, message: Message):
        if message.author.id == self.bot.user.id:
            return

        if isinstance(message.channel, Thread):
            thread = message.channel
            user_id = thread.name[-19:-1]

            if not message.channel.parent_id == modmail_forum_id:
                return

            try:
                user = await self.bot.get_or_fetch_user(user_id)
            except HTTPException:
                print()
            try:

                files = []
                for attachment in message.attachments:
                    files += await attachment.to_file(description=f"From {user.name} ({user.id})")

                await user.send(
                    files=files,
                    embeds=message.embeds,
                    content=message.content,
                    stickers=message.stickers,
                    components=message.components
                )

            except Exception as e:
                await message.add_reaction("⚠️")
                await thread.send(f"```{e}``` User id -> {user_id}")

            else:
                await message.add_reaction("✔️")


def setup(bot: Bot) -> None:
    bot.add_cog(ModMail(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
