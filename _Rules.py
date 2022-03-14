#правила BreadixWorld
import disnake
from enum import Enum
from disnake.ext import commands

#Вы можете свободно добавлять, убирать, изменять пункты правил. В формате:
#"<Номер пункта>_заголовок":"<Заголовок>"
#"<Номер пункта>_содержание":"<Текст/содержание правила>"
rules_texts = {
	"1_заголовок":"Уважайте правила сообщества",
	"1_содержание":"Любые попытки обхода правил этого сервера запрещены, также как и их обсуждение. Если вы заметили какую-то недоработку или ошибку — сообщите о ней администратору.",
	
	"2_заголовок":"Уважайте собеседников",
	"2_содержание":"Никаких оскорблений, провокаций, дискриминации, угроз в реальной жизни и прочего неконструктивного поведения. Если собеседник нарушает это правило, не нужно отвечать в той же манере добавьте нарушителя в игнор и/или обратитесь к модератору или администратору.",
	
	"3_заголовок":"Общайтесь без мата",
	"3_содержание":"Использование ненормативной лексики, в том числе в завуалированном виде – запрещено. Это также касается текста на картинках, аватарках или в именах.",
	
	"4_заголовок":"Общайтесь по делу",
	"4_содержание":"Не следует общаться и тем более спорить в чате на политические, религиозные или личные темы.",
	
	"5_заголовок":"Не мешайте другим игрокам в чате",
	"5_содержание":"Не флудите, не пишите КАПСОМ, не используйте слишком много эмодзи в своих сообщениях.",
	
	"6_заголовок":"Не рекламируйте сторонние сообщества",
	"6_содержание":"Запрещено публиковать в каналах сервера ссылки на сообщества, не относящиеся к BreadixWorld.",
	
	"7_заголовок":"Не попрошайничейте",
	"7_содержание":"Запрещена любая форма попрошайничества на сервере.",
	
	"8_заголовок":"Не выдавайте себя за чужое лицо",
	"8_содержание":"Запрещена выдача себя как за какого-либо члена Администрации, так и за любого другого человека.",
	
	"9_заголовок":"Не обсуждайте блокировки",
	"9_содержание":"В каналах запрещено обсуждение дисциплинарных мер, наложенных как на игровом сервере, так и на сервере Discord или другой официальной площадке. Если вы не согласны с полученными ограничениями, обратитесь в лс [группы ВКонтакте](http://vk.me/breadixhelp).",
	
	"10_заголовок":"Соблюдайте возрастной рейтинг 12+",
	"10_содержание":"Не постите «взрослый» или шок-контент. Это касается всего: текста сообщения, эмодзи, картинок, информации по ссылке, ваших аватарок или имен. Под запретом не только сексуальные темы, но и изображения жестокого обращения с людьми или животными, а также резко неприятные или провокационные изображения.",
	
	"11_заголовок":"Соблюдайте предназнаючение каналов",
	"11_содержание":"В закрепленных сообщениях каждого канала есть описание, для какого рода обсуждений он предназначен. Если вы не знаете, к какому каналу относится ваш вопрос, вы можете спросить у модератора или администратора.",
	
	"12_заголовок":"Соблюдайте правила платформы Discord",
	"12_содержание":"Любые действия, нарушающие [правила платформы Discord](https://discord.com/guidelines), считаются крайне серьёзным нарушением и наказываются соответствующе.",
}
number_of_rules = round(len(rules_texts)/2)

class RulesCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.bot.user} | {__name__}")
	
	@commands.command(name="все-правила")
	@commands.is_owner()
	async def all_rules(self, ctx: commands.Context):
		"""Отправить все правила в чат."""
		rules_embed = disnake.Embed(title="Правила сообщества в Discord")
		#Добавляем все пункты правил к ембеду
		for clause in range(1, number_of_rules):
			rules_embed.add_field(
				name=f"{clause}. {rules_texts[str(clause)+'_заголовок']}",
				value=rules_texts[str(clause)+'_содержание']
			)
		rules_embed.set_footer(text="Некоторые ситуации могут решаться на усмотрение администратора.")
		#Делаем ембед с изображением
		picture_embed = disnake.Embed()
		picture_embed.set_image(url="https://media.discordapp.net/attachments/914829522929614869/916700023541080074/20210629-105623.png")
		#состовляем список из двух ембедов, для отправки в одном сообщении
		embeds = (picture_embed, rules_embed)
		await ctx.send(embeds=embeds)
	
	@commands.slash_command(name="правила")
	async def rule(self, inter: disnake.ApplicationCommandInteraction):
		pass
	
	Rules_clauses = {}
	for clause in range(1, number_of_rules):
		clause_to_add = {f"{clause}. {rules_texts[str(clause)+'_заголовок']}": clause}
		Rules_clauses.update(clause_to_add)
	Rules_clauses = commands.option_enum(Rules_clauses)
	
	async def convert_number(self, number) -> str:
		"""Вернуть изменённое число в русской речевой форме."""
		if number in [1, 4, 5, 9, 0]:
			number = f"{number}-ый"
			return number
		elif number in [2, 6, 7, 8]:
			number = f"{number}-ой"
			return number
		elif number == 3:
			number = f"{number}-ий"
			return number
	
	@rule.sub_command(name="отправить")
	async def rule_clause(
		self,
		inter: disnake.ApplicationCommandInteraction,
		пункт: Rules_clauses,
		упоминание: disnake.User = None
	):
		"""Отправить пункт правил.
		
		Parameters
		----------
		пункт: Выберите пункт правил который будет отправлен.
		упоминание: Упоминуть пользователя в сообщениии.
		"""
		clause = пункт
		member = упоминание
		number = await self.convert_number(clause)
		clause_embed = disnake.Embed(title=f"{number} пункт правил discord сообщества")
		#добавляем только один пункт к ембеду
		clause_embed.add_field(
			name=f"{rules_texts[str(clause)+'_заголовок']}",
			value=rules_texts[str(clause)+'_содержание']
		)
		if member != None:
			await inter.response.send_message(content=f":wave: {member.mention}", embed=clause_embed)
		else:
			await inter.response.send_message(embed=clause_embed)

def setup(bot):
	bot.add_cog(RulesCog(bot))
	print(f" + {__name__}")

def teardown (bot):
	print(f" – {__name__}")