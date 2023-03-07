import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

"""Вы можете свободно добавлять, убирать, изменять пункты правил. В формате:
"<Номер пункта>_заголовок":"<Заголовок>"
"<Номер пункта>_содержание":"<Текст/содержание правила>"""
rules_texts = {
    "1_заголовок": "Поддерживайте это место в чистоте. ",
    "1_содержание": "Общайтесь без мата. Никого не привоцируйте и не оскорбляйте. "
                    "Ничего не попрошайничайте, не рекламируйте и не продавайте. "
                    "Также не нужно всех приглашать на свой сервер.",

    "2_заголовок": "Общайтесь только на русском.",
    "2_содержание": "Это нужно в целях модерации. "
                    "Также, это не сервер поддержки, если нужно - посмотрите во <#610742443847057408>",

    "3_заголовок": "Используйте каналы по назначению.",
    "3_содержание": "Если чувствуете себя потерянными - спросите то, что вы ищите.",

    "4_заголовок": "Оставьте ваши никнеймы легко читаемыми.",
    "4_содержание": "Не используйте кодировки, которые изменяют размер, не дают его прочитать или упомянуть.",

    "5_заголовок": "Без троллинга.",
    "5_содержание": "Троллинг - намеренное, явное поведение с целью опозорить самого себя.",

    "6_заголовок": "Никакого взрослого материала.",
    "6_содержание": "Никакого взрослого, вызывающего, шокирующего, отталкивающего материала.",

    "7_заголовок": "Уважайте других участников.",
    "7_содержание": "Не мешайте другим пользователям. Не включайте музыкальных ботов без согласия участников.",

    "8_заголовок": "Будьте благодарны.",
    "8_содержание": "Не обсуждайте персонал, правила или блокировки. Недопустимо нарушать правила проекта или "
                    "обходить блокировки.",

    "9_заголовок": "Соблюдайте Условия использования и Правила сообщества Discord.",
    "9_содержание": "Вот некоторые из них: \n"
                    "**А.** Соблюдайте ограничение с 13-ти лет.\n"
                    "**Б.** Не выдавайте себя за чужое лицо\n"
                    "**В.** Никакой нетерпимости или принижения.\n"
                    "**Г.** Никаких читов, хаков, вирусов.\n"
                    "**Д.** Никакого косвенного или наводящего на размышления угрозы, угрозы или использование "
                    "чьей-либо личной информацией (также известной как деанон).\n"
                    "**Е.** Не обходите личные блокировки. Не стоит упоминать или преследовать человека, который явно "
                    "дал понять, что не хочет с вами связываться."
}
number_of_rules = round(len(rules_texts) / 2)
class Dropon(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label="Red", description="Your favourite colour is red", emoji="🟥"
            ),
            disnake.SelectOption(
                label="Green", description="Your favourite colour is green", emoji="🟩"
            ),
            disnake.SelectOption(
                label="Blue", description="Your favourite colour is blue", emoji="🟦"
            ),
        ]
        super().__init__(
            placeholder="Choose your favourite colour...",
            min_values=1,
            max_values=1,
            options=options,
        )


    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.send_message(f"Your favourite colour is {self.values[0]}")


def convert_number(number: int) -> str:
    """Вернуть изменённое число в русской речевой форме."""
    if number in [1, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
        number = f"{number}-ый"
        return number
    elif number in [2, 6, 7, 8]:
        number = f"{number}-ой"
        return number
    elif number == 3:
        number = f"{number}-ий"
        return number


class RulesCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} | {__name__}")

    @commands.slash_command(name="правила-проекта")
    async def rule(self, inter: ApplicationCommandInteraction):
        pass

    @commands.slash_command(name="правила-discord")
    async def rules(self, inter: ApplicationCommandInteraction):
        await inter.response.send_message("выв")

    Rules_clauses = {}
    for clause in range(1, number_of_rules + 1):
        clause_to_add = {f"{clause}. {rules_texts[str(clause) + '_заголовок']}": clause}
        Rules_clauses.update(clause_to_add)
    Rules_clauses = commands.option_enum(Rules_clauses)

    @rule.sub_command(name="отправить")
    async def rule_clause(self, inter: ApplicationCommandInteraction, пункт: Rules_clauses,
                          упоминание: disnake.User = None):
        """Отправить пункт правил.

        Parameters
        ----------
        пункт: Выберите пункт правил который будет отправлен.
        упоминание: Кто должен обратить внимание на это правило?
        """
        clause = пункт
        member = упоминание
        clause_embed = disnake.Embed(
            title=f"{clause}. {rules_texts[str(clause) + '_заголовок']}",
            description=rules_texts[str(clause) + '_содержание']
        )#.set_footer(
        #    text=f"{convert_number(clause)} правило сообщества"
        #)
        if member is not None:
            await inter.response.send_message(content=f":wave: {member.mention}", embed=clause_embed)
        else:
            await inter.response.send_message(embed=clause_embed)


def setup(bot):
    bot.add_cog(RulesCog(bot))
    print(f" + {__name__}")


def teardown(bot):
    print(f" – {__name__}")
