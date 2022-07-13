# noinspection PyUnresolvedReferences
import disnake
from disnake.ext import commands


class AntiProfanityCog(commands.Cog):
    """Борьба с ненормативной лексикой"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    profanity_words = []

    async def is_profanity(self, text) -> bool:
        """Вернуть значение есть ли мат в тексте."""
        phrase = text.lower().replace(" ", "")

        def distance(a, b):
            """Вычеслить расстояние Левенштейна между а и б"""
            n, m = len(a), len(b)
            if n > m:
                # Убедиться что n <= m, чтобы использовать O(мин(n, m))
                a, b = b, a
                n, m = m, n

            current_row = range(n + 1)  # Keep current and previous row, not entire matrix
            for i in range(1, m + 1):
                previous_row, current_row = current_row, [i] + [0] * n
                for j in range(1, n + 1):
                    add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                    if a[j - 1] != b[i - 1]:
                        change += 1
                    current_row[j] = min(add, delete, change)

            return current_row[n]

    async def get_profanity(self, text) -> str:
        """Вернуть нецензурные слова."""

    async def check_profanity(self, text) -> str | None:
        """Вернуть слово или """

    # @commands.Cog.listener()
    # async def on_message(self, message):
        # """"""


def setup(bot):
    bot.add_cog(AntiProfanityCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
