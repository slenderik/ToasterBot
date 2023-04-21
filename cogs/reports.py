from asyncio import sleep

from disnake import Message, Embed, ButtonStyle, MessageInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot, Cog
from disnake.ui import View, button, Button


class SupportReportView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(emoji="⚠️", label="Причины отклонения жалоб", style=ButtonStyle.gray,
            custom_id="support_reports:decline_reasons")
    async def support_reports_decline_reasons(self, button: Button, inter: MessageInteraction):
        embed = Embed(title="❓ Почему жалоба может быть отклонена")
        embed.add_field(
            name="1. Недостаточно доказательств",
            value="Иногда для блокировки нарушителя недостаточно одного скриншота. Жалобы, где доказательством является видео, принимаются чаще.",
            inline = False
        )
        embed.add_field(
            name="2. Некорректность формы",
            value="Некорректно написанный ник, не указанный номер сервера мини-игры также могут быть причиной не принятия жалобы.",
            inline=False
        )
        embed.add_field(
            name="3. Нарушитель замечен в основном хабе",
            value="Здесь рассматриваются нарушения, замеченные только на мини-играх.",
            inline=False
        )
        embed.add_field(
            name="4. Доказательства отправлены документом",
            value="Жалобы, в которых доказательства отправлены документом, не рассматриваются. ",
            inline=False
        )
        embed.add_field(
            name="5. Обрезанный скриншот чата",
            value="Принимаются только полные скриншоты чата, не отредактированные на конкретные нарушения.",
            inline=False
        )
        embed.add_field(
            name="6. Жалоба на персонал проекта",
            value="Все недовольства касательно работы персонала проекта (Helper, Moderator, Owner) рассматриваются исключительно в [технической поддержке](https://vk.com/breadixhelp).",
            inline=False
        )

        await inter.response.send_message(embed=embed, ephemeral=True)


class SupportReports(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.persistent_views_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.persistent_views_added:
            self.bot.add_view(SupportReportView())
            self.persistent_views_added = True

        print(f"{self.bot.user} | {__name__}")

    @commands.Cog.listener()
    async def on_message(self, message: Message):

        support_report_channel_id = 1098908853460025366  # TODO Обновить айдишкки к бд
        if message.channel.id != support_report_channel_id or message.author.bot or message.author.id == self.bot.user.id:
            return

        async for msg in message.channel.history(limit=10):
            if msg.author.id == self.bot.user.id:
                await msg.delete()

        embed = Embed(
            title="Жалоба на игрока",
            description="`1.` Напишите ник нарушителя. \n"
                        "`2.` Название и номер сервера, на котором был замечен нарушитель. \n"
                        "`3.` Прикрепите Скриншот или короткий видеоролик на котором зафиксировано нарушение и отчетливо виден ник нарушителя."
        )
        embed.set_footer(
            text="✅ - жалоба отправлена; ⚠️ - жалоба отклонена."
        )
        await message.channel.send(embed=embed, view=SupportReportView())

        if message.content != "" and message.attachments != []:
            # отправляем в канал с репортами
            helper_channel_id = 1098920646421004349  # TODO Обновить айдишкки к бд
            files = [await file.to_file() for file in message.attachments]

            text = ""
            for file in message.attachments:
                print(file.content_type)
                if file.content_type in [""]:
                    text += file.url + '\n'

            helper_channel = self.bot.get_channel(helper_channel_id)
            await helper_channel.send(
                f"**Жалоба**"
                f"\n> {message.content}"
                f"\nОт {message.author.display_name} ({message.author.mention})"
                f"\n[Скачать видео]({message.attachments[0].proxy_url})",
                files=files,
                suppress_embeds=False
            )

            await message.author.send("Жалоба принята к рассмотрению, спасибо, рассмотрим и примем меры.")
            await message.add_reaction("✅")
            await message.add_reaction("😍")
            await sleep(3)
            await message.delete()

        else:
            embed = Embed(
                title="Добавьте фото или видео",
                description="В <#1074695903157432431> принимаем жалобы только с доказательствами. "
                            "Прикрепите фото или видео для жалобы на игрока."
                            f"\n [Сообщение удалится через минуту.]({message.jump_url})"
            )
            await message.author.send(embed=embed)
            await message.add_reaction("⚠️")
            await sleep(3)
            await message.delete()
            await message.author.send(embed=embed)

    @commands.command()
    async def debug_reports(self, ctx: commands.Context):
        embed = Embed(
            title="Жалоба на игрока",
            description="`1.` Напишите ник нарушителя. \n"
                        "`2.` Название и номер сервера, на котором был замечен нарушитель. \n"
                        "`3.` Прикрепите Скриншот или короткий видеоролик на котором зафиксировано нарушение и отчетливо виден ник нарушителя."
        )
        embed.set_footer(
            text="✅ - жалоба отправлена; ⚠️ - жалоба отклонена."
        )
        await ctx.channel.send(embed=embed, view=SupportReportView())


def setup(bot: Bot) -> None:
    bot.add_cog(SupportReports(bot))
    print(f" + {__name__}")


def teardown(bot: Bot) -> None:
    print(f" – {__name__}")
