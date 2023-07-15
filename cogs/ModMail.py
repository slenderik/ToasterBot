import asyncio
import datetime

from disnake import ApplicationCommandInteraction, Message, DMChannel, Thread, NotFound, HTTPException, Thread, User, \
    Member, ForumChannel
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog

modmail_forum_id: int = 1118969274527133808


class ModMail(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    async def get_modmail_thread(self, user: User | Member) -> Thread | None:
        thread = None
        modmail_forum = self.bot.get_channel(modmail_forum_id)
        for mod_thread in modmail_forum.threads:
            if (str(user.id) in mod_thread.name) and (not mod_thread.archived):
                thread = mod_thread
                break

        return thread

    @commands.Cog.listener("on_typing")
    async def on_user_typing(self, channel, user, when: datetime.datetime):
        thread = await self.get_modmail_thread(user)

        if thread is None:
            return

        if thread.parent_id == modmail_forum_id:
            return

        await thread.trigger_typing()

    @commands.Cog.listener("on_typing")
    async def on_agent_typing(self, channel, user, when: datetime.datetime):
        if not channel.parent_id == modmail_forum_id:
            return

        dm = await user.create_dm()

        await dm.trigger_typing()

    @commands.Cog.listener("on_message")
    async def dm_forum(self, message: Message):
        """DM -> FORUM"""

        # denied cyclings
        if message.author.id == self.bot.user.id:
            return

        # only direct message
        if not isinstance(message.channel, DMChannel):
            return

        modmail_forum: Thread
        modmail_forum = self.bot.get_channel(modmail_forum_id)
        user = message.author

        if modmail_forum is None:
            return

        thread = await self.get_modmail_thread(user)

        if thread is None:
            thread, message = await modmail_forum.create_thread(
                name=f"{user.name} ({user.id})",
                content=">>>" + message.content
            )

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
