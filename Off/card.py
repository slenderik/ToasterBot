# noinspection PyUnresolvedReferences
import io
import disnake
from disnake.ext import commands
import aiohttp
from PIL import Image, ImageFont, ImageDraw


class LevelingCog(commands.Cog):
    """Система уровней"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command()
    async def card(self, inter: disnake.ApplicationCommandInteraction):
        """Получить карточки игрока"""
        img = Image.new('RGBA', (400, 200), '#232529')

        async def get_image(url) -> object:
            """Вернуть фотографию аватарки"""
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    if r.status == 200:
                        bytes = io.BytesIO(r._body)
                        return bytes

        response = await get_image(str(inter.author.default_avatar.url))
        response = Image.open(response)
        response = response.convert('RGBA')
        response = response.resize((100, 100), Image.ANTIALIAS)

        img.paste(response, (15, 15, 115, 115))
        idraw = ImageDraw.Draw(img)

        headline = ImageFont.truetype('arial.ttf', size=20)
        undertext = ImageFont.truetype('arial.ttf', size=12)

        idraw.text((145, 15), f'{inter.author.display_name}#{inter.author.display_name}', font=headline)
        idraw.text((145, 50), f'ID: {inter.author.id}', font=undertext)

        img.save('user_card.png')

        await inter.send(file=(disnake.File(fp='user_card.png')))



def setup(bot):
    bot.add_cog(LevelingCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
