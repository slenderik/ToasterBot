#правила BreadixWorld
import disnake
from coffe import color
from disnake.ext import commands

class RulesCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.color = color
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.bot.user} | /правила")
		

	'''Вы можете свободно добавлять, убирать, изменяить любой пункт. В формате:
	<Номер пункта>:<Заголовок>
	<Номер пункт-1>:<Текст/содержание правила>
	'''
	rules_text = {
		1:"Уважайте правила сообщества",
		"1-1":"Любые попытки обхода правил этого сервера запрещены, также как и их обсуждение. Если вы заметили какую-то недоработку или ошибку — сообщите о ней администратору.",
		
		2:"Уважайте собеседников",
		"2-1":"Никаких оскорблений, провокаций, дискриминации, угроз в реальной жизни и прочего неконструктивного поведения. Если собеседник нарушает это правило, не нужно отвечать в той же манере добавьте нарушителя в игнор и/или обратитесь к модератору или администратору.",
		
		3:"Общайтесь без мата",
		"3-1":"Использование ненормативной лексики, в том числе в завуалированном виде – запрещено. Это также касается текста на картинках, аватарках или в именах.",
		
		4:"Общайтесь по делу",
		"4-1":"Не следует общаться и тем более спорить в чате на политические, религиозные или личные темы.",
		
		5:"Не мешайте другим игрокам в чате",
		"5-1":"Не флудите, не пишите КАПСОМ, не используйте слишком много эмодзи в своих сообщениях.",
		
		6:"Не рекламируйте сторонние сообщества",
		"6-1":"Запрещено публиковать в каналах сервера ссылки на сообщества, не относящиеся к BreadixWorld.",
		
		7:"Не попрошайничейте",
		"7-1":"Запрещена любая форма попрошайничества на сервере.",
		
		8:"Не выдавайте себя за чужое лицо",
		"8-1":"Запрещена выдача себя как за какого-либо члена Администрации, так и за любого другого человека.",
		
		9:"Не обсуждайте блокировки",
		"9-1":"В каналах запрещено обсуждение дисциплинарных мер, наложенных как на игровом сервере, так и на сервере Discord или другой официальной площадке. Если вы не согласны с полученными ограничениями, обратитесь в лс [группы ВКонтакте](http://vk.me/breadixhelp).",
		
		10:"Соблюдайте возрастной рейтинг 12+",
		"10-1":"Не постите «взрослый» или шок-контент. Это касается всего: текста сообщения, эмодзи, картинок, информации по ссылке, ваших аватарок или имен. Под запретом не только сексуальные темы, но и изображения жестокого обращения с людьми или животными, а также резко неприятные или провокационные изображения.",
		
		11:"Соблюдайте предназнаючение каналов",
		"11-1":"В закрепленных сообщениях каждого канала есть описание, для какого рода обсуждений он предназначен. Если вы не знаете, к какому каналу относится ваш вопрос, вы можете спросить у модератора или администратора.",
		
		12:"Соблюдайте правила платформы Discord",
		"12-1":"Любые действия, нарушающие [правила платформы Discord](https://discord.com/guidelines), считаются крайне серьёзным нарушением и наказываются соответствующе.",
	}
	number_of_rules = round(len(rules_text)/2)
	
	@commands.command()
	@commands.is_owner()
	async def rules(self, ctx: commands.Context):
		
		emb = disnake.Embed(
			title="Правила сообщества в Discord",
			colour=self.color,
		)
		'''Добавляем к ембеду все пункты правил'''
		for i in range(1, self.number_of_rules):
			emb.add_field(
				name=f"{i}. {self.rules_text[i]}",
				value=self.rules_text[(str(i)+"-1")]
			)
		
		emb.set_footer(text="Ситуации, которые не прописаны в этом своде правил, администрация решает на свое усмотрение.")
		#Делаем ембед с изображением
		
		pic = disnake.Embed(colour=self.color)
		pic.set_image(url="https://media.discordapp.net/attachments/914829522929614869/916700023541080074/20210629-105623.png")
		#состовляем список из двух ембедов, для последовательной отправки в одном сообщении
		embeds = (pic, emb)
		await ctx.send(embeds=embeds)
	
	@commands.slash_command(name="правила")
	async def rule_clause(
		self,
		inter: disnake.ApplicationCommandInteraction,
		пункт: int = commands.Param(min_value=1, max_value=number_of_rules),
	):
		"""Отправляет правила
		
		Parameters
		----------
		пункт: Выберите конкретный пункт (1-12)
		"""
		#Текст выше является описание команды и аргумента Пункт
		emb = disnake.Embed(title=f"{пункт}-ый пункт правил сообщества", colour=self.color)
		#добавляем только один пункт к ембеду
		emb.add_field(
			name=f"{self.rules_text[пункт]}",
			value=self.rules_text[str(пункт)+"-1"],
		)
		await inter.response.send_message(embed=emb)

def setup(bot):
	bot.add_cog(RulesCog(bot))
	print(f" + {__name__}")

def teardown (bot):
	print(f" – {__name__}")