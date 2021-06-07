from os import error
import random
import asyncpg
import discord
from discord import message
from discord.colour import Color
from discord.ext import commands, tasks
import time
from discord.ext.commands.core import command

from discord.ext.commands.errors import MemberNotFound

# Stolen from https://stackoverflow.com/a/20007730. Thanks!
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

class UserBeanAccount:
	def __init__(self, user, balance):
		self.user = user
		self.touched = time.monotonic()
		self.needs_db_commit = False

		# Default balance!
		# If the db returns a None somehow when the user has a balance, well that's just unlucky :P
		if balance is None:
			balance = 100

		self.balance = balance
	
	def touch(self):
		self.touched = time.monotonic()

	def set(self, amount):
		if amount > 0:
			self.balance = amount
		else:
			self.balance = 0
		self.needs_db_commit = True
		self.touch()
	
	def add(self, amount):
		if amount > 0:
			self.balance = self.balance + amount
			self.needs_db_commit = True
			self.touch()

	def remove(self, amount):
		if amount > 0:
			self.balance = self.balance - amount
			self.needs_db_commit = True
			self.touch()

class BeansEconomyCog(commands.Cog, name='BeansV2'):
	def __init__(self, bot, db_url):
		self.bot = bot
		self.db_url = db_url
		self.account_cache = {}
		self.commit_updates_to_db.add_exception_type(asyncpg.PostgresConnectionError)
		self.is_connected = False
		self.leaderboard_embed = None

	def cog_unload(self):
		self.commit_updates_to_db.cancel()

	async def cog_before_invoke(self, ctx):
		if not self.is_connected or self.conn.is_closed():
			# connect to the database
			self.conn = await asyncpg.connect(self.db_url)
			
			# ensure our data schema exists
			await self.conn.execute("""
				CREATE TABLE IF NOT EXISTS beans_balance (
					discord_snowflake BIGINT UNIQUE PRIMARY KEY,
					beans INTEGER NOT NULL);
			""")

			# set the connected flag
			print("Connected to the DB!")
			self.is_connected = True
			self.commit_updates_to_db.start()

	async def get_user_account(self, user:discord.Member):
		if user.id in self.account_cache:
			return self.account_cache[user.id]

		# If this is still a None by the time we create the account, this user is considered "new"
		current_balance = None

		db_row = await self.conn.fetchrow("""
			SELECT (beans)
			FROM beans_balance
			WHERE discord_snowflake = $1
		""", user.id)

		# If the user *has* a row, we need to make sure we get the balance.
		if db_row is not None:
			current_balance = db_row.get("beans")

		balance_object = UserBeanAccount(user.id, current_balance)
		self.account_cache[user.id] = balance_object

		return balance_object

	#Personal

	@commands.command(aliases=["bal"])
	async def balance(self, ctx):
		balance = await self.get_user_account(ctx.message.author)
		
		embed = discord.Embed(title=f"Account ID={ctx.author.name}", description=f"You have {balance.balance} beans in the bank", color = ctx.author.color)
		embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/173/173819.png")

		await ctx.send(embed=embed)

	@commands.command()
	async def hax(self, ctx, user: discord.Member = None):
		if user == None:
			await ctx.send("You must mention someone!")
			return
		elif user == ctx.message.author:
			await ctx.send("Use balance command for your own ammount :P")
			return
		balance = await self.get_user_account(user)
		embed = discord.Embed(title=f"Account ID={user.name}", description=f"{user.name} has {balance.balance} beans in the bank", color=discord.Color.red())
		embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/173/173819.png")	
		
		await ctx.send(embed=embed)

	@commands.command()
	async def transfer(self, ctx, other_user: discord.Member, amount: int = None):
		
		if amount == None:
			amount = 1			
				
		if amount <= 0:
			await ctx.send("Invalid amount")
			return

		source_account = await self.get_user_account(ctx.message.author)
		destination_account = await self.get_user_account(other_user)

		if source_account.balance < amount:
			await ctx.send("You cannot afford this transaction")
		else:
			source_account.remove(amount)
			destination_account.add(amount)
						
			await ctx.send("Transaction complete")

	#Self Commands
	
	@commands.command()
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def work(self, ctx):
		account = await self.get_user_account(ctx.message.author)
		earned = random.randint(50, 250)
		account.add(earned)

		embed = discord.Embed(title="Work Work Work!", description=f"You worked hard and got {earned} beans", color = ctx.author.color)
		embed.set_thumbnail(url="https://freepikpsd.com/wp-content/uploads/2019/10/tin-of-beans-png-transparent-tin-of-beanspng-images-pluspng-png-baked-beans-650_650.png")

		await ctx.send(embed=embed)

	@work.error
	async def work_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = "You can only work once every hour \n Next work will be avaible in: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="Bro chill!", description=f"{msg}", color = ctx.author.color)    
			embed.set_thumbnail(url="http://cdn.onlinewebfonts.com/svg/img_571830.png")
			await ctx.send(embed=embed)
		else:
			raise error

	@commands.command()
	@commands.cooldown(1, 43200, commands.BucketType.user)
	async def steal(self, ctx, other_user: discord.Member, amount: int = None,):
		
		Chance = random.randint(-10, 10)
		thief = await self.get_user_account(ctx.message.author)
		victim = await self.get_user_account(other_user)

		if amount == None:
			await ctx.send("Enter an ammount")
			self.steal.reset_cooldown(ctx)
			return
		if other_user == None:
			await ctx.send("Who is the victim?")
			self.steal.reset_cooldown(ctx)
			return		

		if amount <= 0:
			await ctx.send("Invalid amount")
			self.steal.reset_cooldown(ctx)
			return

		if amount > 150:
			await ctx.send("Stealing more than 150 beans is too risky! Just forget it...")
			self.steal.reset_cooldown(ctx)
			return	
	
		if victim.balance < amount:
			await ctx.send("Come on! They are poor enough...")
			self.steal.reset_cooldown(ctx)
			return
		else:
			if Chance > 0:
				victim.remove(amount)
				thief.add(amount)
				await ctx.send("Just like GTA...")
			if Chance <= 0:
				thief.remove(amount)
				victim.add(amount)
				await ctx.send("BUSTED - You lost the amount you tried to steal")        
	@steal.error
	async def steal_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			stl = "Gotta wait 12h \n I think you should wait for: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="Let's not...", description=f"{stl}", color = ctx.author.color)    
			embed.set_thumbnail(url="https://pngimg.com/uploads/prison/prison_PNG45.png")
			await ctx.send(embed=embed)
		else:
			raise error
	
	@commands.command()
	@commands.cooldown(1, 600, commands.BucketType.user)
	async def beg(self, ctx):
		account = await self.get_user_account(ctx.message.author)
		earned = random.randint(0, 50)
		account.add(earned)

		embed = discord.Embed(title="Gib Monex!", description=f"Well... If you don't wanna work {earned} beans", color = ctx.author.color)
		embed.set_thumbnail(url="https://img.icons8.com/ios/452/beggar.png")

		await ctx.send(embed=embed)

	@beg.error
	async def beg_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			beg = "Lazy one eh? But you gotta wait begga \n Next beg will be avaible in: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="But! Wait!!", description=f"{beg}", color = ctx.author.color)    
			embed.set_thumbnail(url="https://img.icons8.com/ios/452/white-beans.png")
			await ctx.send(embed=embed)
		else:
			raise error

	@commands.command()
	@commands.cooldown(1, 864000, commands.BucketType.user)
	async def daily(self, ctx):
		account = await self.get_user_account(ctx.message.author)
		beanz = [1, 50, 100, 200, 300]
		dailyv = random.choice(beanz)
		account.add(dailyv)

		embed = discord.Embed(title="Daily", description=f"I am a good bot. So I will give you  {dailyv} beans for today", color = ctx.author.color)
		embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/17/17538.png")

		await ctx.send(embed=embed)
	@daily.error
	async def daily_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			beg = "No!  \n Wait for: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="It's called Daily", description=f"{beg}", color = ctx.author.color)    
			embed.set_thumbnail(url="https://img.icons8.com/ios/452/white-beans.png")
			await ctx.send(embed=embed)
		else:
			raise error

	@commands.command()
	@commands.cooldown(1, 1800, commands.BucketType.user)
	async def adventure(self, ctx):
		account = await self.get_user_account(ctx.message.author)
		adv = [-100, -50, 50, 100, 200, 300]
		advv = random.choice(adv)
		account.add(advv)

		if advv < 0:
			embed = discord.Embed(title="Adventure Time!", description=f"Sadly you couldn't find anything and hurt yourself, Hospital bill costed {advv} beans")
			embed.set_thumbnail(url="https://img.pngio.com/medic-png-3-png-image-medic-png-600_600.png")
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title="Adventure Time!", description=f"You went out for and adventure and found {advv} beans worth of tressure", color = ctx.author.color)
			embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/17/17538.png")
			await ctx.send(embed=embed)
	@adventure.error
	async def adventure_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			ad = "You have to rest!  \n Wait for: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="It's called Daily", description=f"{ad}", color = ctx.author.color)    
			embed.set_thumbnail(url="https://icon2.cleanpng.com/20180205/otq/kisspng-viking-sword-shield-weapon-sword-shield-png-pic-5a7918e485de54.9837911315178856685483.jpg")
			await ctx.send(embed=embed)
		else:
			raise error
	
	#Gamble
	
	@commands.command()
	@commands.cooldown(5, 180, commands.BucketType.user)
	async def flip(self, ctx, amount: int = None):
		if amount == None or amount <= 0:
			await ctx.send("You have to give some beans before playing gamble")
			return

		account = await self.get_user_account(ctx.message.author)

		if amount > account.balance:
			await ctx.send("OMG, you can't even affor that :D Why do you even bother?")
			return

		if random.randint(0,1) == 1:
			account.add(amount)
			embed=discord.Embed(title="heads or tails!", description=f"You are lucky! You just won {amount*2} beans", color = ctx.author.color)
			embed.set_thumbnail(url="https://www.pngrepo.com/download/261646/coin-flip.png")
			await ctx.send(embed=embed)
		else:
			account.remove(amount)
			embed = discord.Embed(title="heads or tails!", description=f"Ah unlucky... You lost your bet of {amount} beans", color = ctx.author.color)
			embed.set_thumbnail(url="https://www.pngrepo.com/download/261646/coin-flip.png")
			await ctx.send(embed=embed)

	@flip.error
	async def flip_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			tossv = "You are doing that too often \n Wait for: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="Slow Down", description=f"{tossv}", color = ctx.author.color)    
			embed.set_thumbnail(url="https://www.pngkit.com/png/full/603-6030012_open-11-11-clock-png.png")
			await ctx.send(embed=embed)
		else:
			raise error

	@commands.command()
	@commands.cooldown(5, 180, commands.BucketType.user)
	async def toss(self, ctx, amount: int = None):
		
		A = amount
		
		if amount == None or amount <= 0:
			await ctx.send("You have to give some beans before playing gamble")
			return

		account = await self.get_user_account(ctx.message.author)

		if amount > account.balance:
			await ctx.send("I knew that you were poor. But I though you had intelligence! Bro if you can't afford such a th,ng, why are you gambling?")
			return

		tossv = random.randint(-2*A, 2*A)		
		
		if tossv >0:
			embed=discord.Embed(title="Toss!", description=f"You are lucky! You just won {tossv} beans", color = ctx.author.color)
			embed.set_thumbnail(url="https://www.pngrepo.com/download/261646/coin-flip.png")
			account.add(tossv)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title="Toss!", description=f"Ah unlucky... You lost {tossv} beans", color = ctx.author.color)
			embed.set_thumbnail(url="https://www.pngrepo.com/download/261646/coin-flip.png")
			account.remove(abs(tossv))
			await ctx.send(embed=embed)

	@toss.error
	async def toss_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			tossv = "You are doing that too often \n Wait for: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="Slow Down", description=f"{tossv}", color = ctx.author.color)    
			embed.set_thumbnail(url="https://www.pngkit.com/png/full/603-6030012_open-11-11-clock-png.png")
			await ctx.send(embed=embed)
		else:
			raise error


	@commands.command()
	async def shop(self, ctx):
		shop = [
			{"name":"GAM Mug","price":100,"description":"A Mug for hot ones"},
			{"name":"OC Figure of Mods","price":250,"description":"Show your love to best mods"},
			{"name":"Body Pillow","price":500,"description":"For loners/cultured ones"},
			{"name":"Airsoft Gun","price":10000,"description":"We azre not licanced to sell real one"},
			{"name":"Panzerkampfwagen V","price":1000000,"description":"German Engineering wonder"},
			{"name":"F-35","price":10000000,"description":"World current best jet"}]   
		em = discord.Embed(title = "Shop")

		for item in shop:
			name = item["name"]
			price = item["price"]
			desc = item["description"]
			em.add_field(name = name, value = f"{price} BEANS | {desc}")

		await ctx.send(embed = em)

	async def fetch_leaderboard(self):
		top_10 = await self.conn.fetch("""
			SELECT (discord_snowflake)
			FROM beans_balance
			ORDER BY beans DESC
			LIMIT 10
		""")

		description = ""
		place = 1

		for record in top_10:
			# for if we ever want to show the beans values on the leaderboard.
			# the beans will be out of date due to the way we cache the embed.
			"""
			row = record['row']
			username = "Invalid User"
			user_snowflake = row[0]
			beans = row[1]
			"""

			user_snowflake = record['discord_snowflake']
			user = self.bot.get_user(user_snowflake)

			if user is None:
				try:
					user = await self.bot.fetch_user(user_snowflake)
				except:
					user = None

			if not user is None:
				username = user.name

			description += f"**{ordinal(place)}**: {username}\n"
			place += 1

		self.leaderboard_embed = discord.Embed(title = "Beans Leaderboard", description = description, color = discord.Color.red())

	@commands.command()
	@commands.cooldown(1, 180, commands.BucketType.default)
	async def leaderboard(self, ctx):
		await self.fetch_leaderboard()
		await ctx.send(embed=self.leaderboard_embed)
		
	@leaderboard.error
	async def leaderboard_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			# If we mananged to get into the cooldown without having an embed generated, make sure we still generate it.
			if self.leaderboard_embed is None:
				await self.fetch_leaderboard()
			
			await ctx.send(embed=self.leaderboard_embed)
		else:
			raise error

	#Don't touch rest	

	@commands.command()
	async def add(self, ctx, amount:int, target:discord.Member):
		if await self.bot.is_owner(ctx.message.author):
			target_balance = await self.get_user_account(target)

			# we're using set so we can actually add negative amounts if we want...
			target_balance.set(target_balance.balance + amount)
			await ctx.send("Beanzzz!!")
		else:
			await ctx.send("You don't have permission to do that!")

	@tasks.loop(seconds=10.0)
	async def commit_updates_to_db(self):
		# we can only commit to the database when it's available!
		if self.conn and not self.conn.is_closed():
			if len(self.account_cache) == 0:
				return

			objects_to_commit = []
			objects_to_free = []
			max_last_update_time = time.monotonic() - 60.0

			for account_obj in self.account_cache.values():
				if account_obj.needs_db_commit:
					objects_to_commit.append(account_obj)
				elif account_obj.touched < max_last_update_time:
					objects_to_free.append(account_obj)

			if len(objects_to_commit) > 0:
				new_rows = []

				for account_obj in objects_to_commit:
					new_rows.append((account_obj.user, account_obj.balance))

				try:
					await self.conn.executemany("""
						INSERT INTO beans_balance(discord_snowflake, beans) 
							VALUES($1, $2) 
							ON CONFLICT (discord_snowflake)
							DO UPDATE
								SET beans = EXCLUDED.beans;
					""", new_rows)

					for account_obj in objects_to_commit:
						account_obj.needs_db_commit = False
				except Exception as e:
					print(e)

			for account_obj in objects_to_free:
				# we check again, just in case
				if not account_obj.needs_db_commit and account_obj.touched < max_last_update_time:
					# remove the reference from the cache meaning that nothing should be able to see this object
					self.account_cache.pop(account_obj.user)
