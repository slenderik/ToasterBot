import disnake
from random import choice
from asyncio import sleep
from toaster import color
from disnake.utils import get
from disnake.ext import commands

custom_rooms = {}

server_id = 823820166478823462

async def get_channel(inter) -> str:
	"""Вернуть канала автора."""
	server = inter.bot.get_guild(server_id)
	owner_channel = custom_rooms[inter.user.id]
	channel = get(server.voice_channels, id=owner_channel)
	return channel

class MurderMusteryButtons(disnake.ui.View):
	pass

class SkyWarsButtons(disnake.ui.View):
	def __init__(self):
		super().__init__()
		self.number = None
	
	@disnake.ui.button(
		label="1",
		style=disnake.ButtonStyle.green
	)
	async def first_server(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		await inter.response.defer()
		self.number = "№1"
		self.stop()
	
	@disnake.ui.button(
		label="2",
		style=disnake.ButtonStyle.green
	)
	async def second_server(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		await inter.response.defer()
		self.number = "№2"
		self.stop()

class BedWarsButtons(disnake.ui.View):
	pass


async def response_status(inter):
	"""вернуть резрешение на продолжение и исключить не благоприятные условия"""
	response_embed = disnake.Embed(color=disnake.Color.default())
	
	#Если человек владелец какого-то канала
	if inter.user.id in custom_rooms:
		#если владелец в канале
		server = inter.bot.get_guild(server_id)
		channel_id = custom_rooms[inter.user.id]
		channel = get(server.voice_channels, id=channel_id)
		users = channel.voice_states
		if inter.user.id in users:
			#возвращаем значения для продолжения итерации
			return True
		
		#если владелец не в канале
		else:
			#отвечаем на итерацию:
			response_embed = disnake.Embed(color=disnake.Color.default())
			response_embed.add_field(
				name="Вы не владелец канала^^",
				value="Если владелец вышел - пропишите `/канал забрать`, для того чтобы стать владелецем."
			)
			await inter.response.send_message(embed=response_embed, ephemeral=True)
			#запрет на продолжение
			return False
		
		#Если человек не влделец какого-то канала
		if inter.user.id not in custom_rooms:
			#ответ на итерацию
			response_embed.add_field(
				name="Зайдите в канал",
				value="Для того чтобы изменить назвние от этого канал - зайдите в него и завново нажмите кнопку"
			)
			await inter.response.send_message(embed=response_embed, ephemeral=True)
			#запрет на продолжение
			return False


class VoiceView(disnake.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		
	@disnake.ui.button(
		label="Общение",
		style=disnake.ButtonStyle.blurple,
		custom_id="voice_view:talk",
		row=0
	)
	async def talk(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		"""Переименовать канал в Общение."""
		accses = await response_status(inter=inter)
		if accses:
			channel = await get_channel(inter=inter)
			name = channel.name
			
			if "🔞" in name:
				name="🔞 Общение"
			else:
				name="Общение"
			
			await channel.edit(name=name, reason="[Собственне каналы] Кнопка управления (ЛС)")
			
			#выключаем кнопку
			button.style = disnake.ButtonStyle.green
			button.disabled = True
			await inter.response.edit_message(view=self)
			
			#отвечаем пользователю
			response_embed = disnake.Embed(
				title=f"Название изменено на {name}!",
				color=disnake.Color.default()
			)
			await inter.response.send_message(embed=response_embed, ephemeral=True)
	
	@disnake.ui.button(
		label="Музыка",
		style=disnake.ButtonStyle.blurple,
		custom_id="voice_view:music",
		row=0
	)
	async def music(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		"""Переименовать канал в Музыка."""
		accses = await response_status(inter=inter)
		if accses:
			channel = await get_channel(inter=inter)
			name = channel.name
			
			if "🔞" in name:
				name="🔞 Музыка"
			else:
				name="Музыка"
			
			await channel.edit(name=name, reason="[Собственне каналы] Кнопка управления (ЛС)")
			
			#выключаем кнопку
			button.style = disnake.ButtonStyle.green
			button.disabled = True
			await inter.response.edit_message(view=self)
			
			#отвечаем пользователю
			response_embed = disnake.Embed(
				title=f"Название изменено на {name}!",
				color=disnake.Color.default()
			)
			await inter.response.send_message(embed=response_embed, ephemeral=True)
	
	@disnake.ui.button(
		label="оффтоп",
		style=disnake.ButtonStyle.blurple,
		custom_id="voice_view:offtop",
		row=0
	)
	async def offtop(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		"""Переименовать канал в Оффтоп."""
		accses = await response_status(inter=inter)
		if accses:
			channel = await get_channel(inter=inter)
			name = channel.name
			
			if "🔞" in name:
				name="🔞 Оффтоп"
			else:
				name="Оффтоп"
			
			await channel.edit(name=name, reason="[Собственне каналы] Кнопка управления (ЛС)")
			
			response_embed = disnake.Embed(
				title=f"Название изменено на {name}!",
				color=disnake.Color.default()
			)
			await inter.response.send_message(embed=response_embed, ephemeral=True)
		
	@disnake.ui.button(
		label="SkyWars",
		style=disnake.ButtonStyle.green,
		custom_id="voice_view:skywars",
		row=1
	)
	async def skywars(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		"""Переименовать канал в SkyWars."""
		accses = await response_status(inter=inter)
		if accses:
			channel = await get_channel(inter=inter)
			name = channel.name
			
			if "🔞" in name:
				name="🔞 SkyWars"
			else:
				name="SkyWars"
			
			await channel.edit(name=name, reason="[Собственне каналы] Кнопка управления (ЛС)")
			
			response_embed = disnake.Embed(
				title=f"Название изменено на {name}!",
				color=disnake.Color.default()
			)
			button = SkyWarsButtons()
			await inter.response.send_message(embed=response_embed, ephemeral=True, view=button)
			await button.wait()
			if button.number is None:
				response_embed = disnake.Embed(title="Время вышло!", color=disnake.Color.default())
				await inter.response.send_message(embed=response_embed, ephemeral=True)
			elif button.number is not None:
				if "🔞" in name:
					name=f"🔞 SkyWars {button.number}"
				else:
					name=f"SkyWars {button.number}"
				
				response_embed = disnake.Embed(title=f"Название изменено на {name}!", color=disnake.Color.default())
				await channel.edit(name=name, reason="[Собственне каналы] Кнопка управления (ЛС)")
				
				await inter.response.send_message(embed=response_embed, ephemeral=True)
		
	@disnake.ui.button(
		label="BedWars",
		style=disnake.ButtonStyle.green,
		custom_id="voice_view:bedwars",
		row=1
	)
	async def bedwars(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		pass
	
	@disnake.ui.button(
		label="Survival",
		style=disnake.ButtonStyle.green,
		custom_id="voice_view:survival",
		row=1
	)
	async def survival(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		pass
	
	@disnake.ui.button(
		label="MurderMustery",
		style=disnake.ButtonStyle.green,
		custom_id="voice_view:murdermustery",
		row=1
	)
	async def murdermustery(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		pass
	
	@disnake.ui.button(
		label="Есть мат",
		style=disnake.ButtonStyle.red,
		custom_id="voice_view:yes_profanity",
		row=2
	)
	async def yes_profanity(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		"""переименовать канал владельца в название со значком мата"""
		accses = await response_status(inter=inter)
		if accses:
			channel = await get_channel(inter=inter)
			
			name = channel.name
			if "🔞" not in name:
				name = f"🔞 {name}"
			
			await channel.edit(name=name, reason="[Собственне каналы] Кнопка управления (ЛС)")
			
			response_embed = disnake.Embed(color=disnake.Color.default())
			response_embed.add_field(
				name=f"Название изменено на {name}!",
				value="Это означает что в канале может быть мат"
			)
			await inter.response.send_message(embed=response_embed, ephemeral=True)
		
		
	@disnake.ui.button(
		label="Без мата",
		style=disnake.ButtonStyle.red,
		custom_id="voice_view:no_profanity",
		row=2
	)
	async def no_profanity(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		"""переименовать канал владельца в название со значком без мата"""
		accses = await response_status(inter=inter)
		if accses:
			channel = await get_channel(inter=inter)
			name = channel.name
			
			if "🔞" in name:
				name = name.replace("🔞", "")
			
			await channel.edit(name=name, reason="[Собственне каналы] Кнопка управления (ЛС)")
			
			response_embed = disnake.Embed(color=disnake.Color.default())
			response_embed.add_field(
				name=f"Название изменено на {name}!",
				value="Это означает что в канале может быть мат"
			)
			await inter.response.send_message(embed=response_embed, ephemeral=True)


class VoiceCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.voice_views_added = False
		self.voice_create_id = 879387831385088020
		self.voice_category_id = 823820166478823466
		self.chat_id = 823820166478823464
		self._cd = commands.CooldownMapping.from_cooldown(1, 10.0, commands.BucketType.member)
		
	def get_ratelimit(self, member):
		"""Вернуть времени задержки"""
		bucket = self._cd.get_bucket(member)
		return bucket.update_rate_limit()

	@commands.Cog.listener()
	async def on_ready(self):
		if not self.voice_views_added:
			self.bot.add_view(VoiceView())
			self.bot.voice_views_added = True
		
		print(f"{self.bot.user} | {__name__}")

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		
		retry_after = self.get_ratelimit(member)
		if retry_after is not None:
			print(retry_after)
		
		expect_embed = disnake.Embed(
			title="Похоже я не могу вам написать...",
			description="Я обычно пишу участникам в Личные Сообщения. НО похоже что-то пошло ни так!",
			colour=disnake.Color.default()
		)
		expect_embed.add_field(
			name="Для чего это надо?",
			value="Для полноценной работы бота\nЯ люблю сообщения видемые только для вас. Но их не всегда возможно использовать и приходится беспокоить вас в личных сообщениях^^"
		)
		expect_embed.add_field(
			name="Как мне открыть?",
			value="Попробуйте:\n1. Включить сообщения от участников сервера. Наш сервер -> троеточие -> Сообщения от участников - включить\n2. Отключить настройки приватности. Настройки -> настройки приватности -> получать сообщения -> от ботов - включить"
		)
		
		#если перешёл/вышел
		#None, если участник не был на этом сервере в голосовых 
		if before.channel != None:
			#если участник вышел из кастомных каналов
			if before.channel.id in custom_rooms:
				#если вышел из кастомного канал последним
				if before.channel.voice_states == {}:
					print("участник вышел из кастомного канала и его НАДО удалить")
					
					#удаляем из списка канал и его создателя-участника
					owner = custom_rooms[before.channel.id]
					custom_rooms.pop(owner)
					custom_rooms.pop(before.channel.id)
					
					await sleep(0.3)
					await before.channel.delete(reason="[собственные каналы] Все участники вышли!")
					try:
						delete_embed = disnake.Embed(title="Выш канал удалён", color=disnake.Color.default())
						dm_member = await member.create_dm()
						await dm_member.send(embed=delete_embed)
					except Exception as e:
						print(e)
						chat = get(after.channel.guild.channels, id=self.chat_id)
						await chat.send(f"{member.mention}",embed=expect_embed)
			
		
		#если участник зашёл/перешёл
		if after.channel != None:
			if after.channel.id == self.voice_create_id:
				print(" 1 - надо создать канал и перекинуть туда человека")
				custom_category = get(after.channel.guild.channels, id=self.voice_category_id)
				overwrites = {member: disnake.PermissionOverwrite(view_channel=True)}
				
				emoji_list = ["👀", "💭", "✨", "❄️", "🌿", "🌠", "🎆", "💞", "🚩", "🌈", "🍞", "🐶", "💮", "🎲", "🤟", "🌼", "🌠", "🎉", "🎂", "🎀", "🎈", "🎁", "🎵", "🎶", "💭"]
				emoji = choice(emoji_list)
				
				channel = await after.channel.guild.create_voice_channel(
					name=f"{member.display_name}{emoji}",
					reason="[собственные каналы] Создание",
					category=custom_category,
					position=after.channel.position+1
				)
				
				#переносим участника в его канал
				await sleep(1)
				await member.move_to(channel, reason="[собственные каналы] Он создал свой канал!")

				#добавляем в список канал и его создателя-участника
				new_channel = {channel.id: member.id, member.id: channel.id}
				custom_rooms.update(new_channel)

				#пишем пользователю с предложением повесить теги
				#<:breadix:940540206866628641>
				try:
					dm_embed = disnake.Embed(
						title="Вы создали канал",
						description=f"Название: {name}!",
						color=disnake.Color.default()
					)
					dm_embed.set_footer(text="Вот некоторые настройки")
					view = VoiceView()
					
					dm_member = await member.create_dm()
					await dm_member.send(embed=dm_embed, view=view)
				except Exception as e:
					print(e)
					chat = get(after.channel.guild.channels, id=self.chat_id)
					await chat.send(f"{member.mention}",embed=expect_embed)
				
				print("создали и переместили")
		print("------------")


def setup(bot):
	bot.add_cog(VoiceCog(bot))
	print(f" + {__name__}")

def teardown(bot):
	print(f" – {__name__}")
