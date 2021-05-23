import random
import asyncpg
import discord
from discord.ext import commands, tasks
import time

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

	def cog_unload(self):
		self.commit_updates_to_db.cancel()

	async def cog_before_invoke(self, ctx):
		if not self.is_connected:
			# connect to the database
			self.conn = await asyncpg.connect(self.db_url)
			
			# ensure our data schema exists
			await self.conn.execute("""
				CREATE TABLE IF NOT EXISTS beans_balance (
					discord_snowflake BIGINT UNIQUE PRIMARY KEY,
					beans INTEGER NOT NULL);
			""")

			# set the connected flag
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

	@commands.command()
	async def balance(self, ctx):
		balance = await self.get_user_account(ctx.message.author)
		await ctx.send(f"You have {balance.balance} beans in the bank")

	@commands.command()
	async def transfer(self, ctx, amount: int, other_user: discord.Member):
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
	@commands.cooldown(1, 864000, commands.BucketType.user)
	async def steal(self, ctx, amount: int, other_user: discord.Member):
		
		Chance = random.randint(-10, 10)
		thief = await self.get_user_account(ctx.message.author)
		victim = await self.get_user_account(other_user)
		
		if amount <= 0:
			await ctx.send("Invalid amount")
			return

		if amount > 150:
			await ctx.send("Too risky. Forget it")
			return	

		if victim.balance < amount:
			await ctx.send("Come on! They are poor enough...")
			return
		else:
			if Chance > 0:
				victim.remove(amount)
				thief.add(amount)
				await ctx.send("Just like GTA")
			if Chance <= 0:
				thief.remove(amount)
				victim.add(amount)
				await ctx.send("BUSTED - You lost the amount you tried to steal")        
	@steal.error
	async def steal_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			stl = "Gotta wait 24h \n I think you should wait for: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="Let's not...", description=f"{stl}", color = ctx.author.color)    
			embed.set_thumbnail(url="https://pngimg.com/uploads/prison/prison_PNG45.png")
			await ctx.send(embed=embed)
		else:
			raise error

	#Gamble
	
	@commands.command()
	@commands.cooldown(1, 600, commands.BucketType.user)
	async def beg(self, ctx):
		account = await self.get_user_account(ctx.message.author)
		earned = random.randint(0, 100)
		account.add(earned)

		embed = discord.Embed(title="Gib Monex!", description=f"Well... If you don't wanna work {earned} beans", color = ctx.author.color)
		embed.set_thumbnail(url="https://img.icons8.com/ios/452/beggar.png")

		await ctx.send(embed=embed)

	@beg.error
	async def beg_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			beg = "You want money money and money eh? But you gotta wait begga \n Next beg will be avaible in: {:.2f}s".format(error.retry_after)
			
			embed = discord.Embed(title="Ahh... Shame", description=f"{beg}", color = ctx.author.color)    
			embed.set_thumbnail(url="http://cdn.onlinewebfonts.com/svg/img_571830.png")
			await ctx.send(embed=embed)
		else:
			raise error

	@commands.command()
	@commands.cooldown(5, 180, commands.BucketType.user)
	async def flip(self, ctx, amount: int = None):
		if amount == None or amount <= 0:
			await ctx.send("You have to give some beans before playing gamble")
			return

		account = await self.get_user_account(ctx.message.author)

		if amount > account.balance:
			await ctx.send("You don't have enough beans")
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
			await ctx.send("You don't have enough beans")
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
			{"name":"GAM Mug","price":100,"description":"A Mug for flip ones"},
			{"name":"OC Figure of Mods","price":250,"description":"Show your love to best mods"},
			{"name":"Body Pillow","price":500,"description":"For loners/cultured ones"}]   
		em = discord.Embed(title = "Shop")

		for item in shop:
			name = item["name"]
			price = item["price"]
			desc = item["description"]
			em.add_field(name = name, value = f"{price} BEANS | {desc}")

		await ctx.send(embed = em)

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
