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
		if amount >= 0:
			self.balance = amount
			self.needs_db_commit = True
			self.touch()
	
	def add(self, amount):
		if amount > 0:
			self.balance = self.balance + amount
			self.needs_db_commit = True
			self.touch()

	def remove(self, amount):
		if amount < 0:
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

		db_row = await self.conn.fetchrow("""
			SELECT (beans)
			FROM beans_balance
			WHERE discord_snowflake = $1
		""", user.id)

		balance_object = UserBeanAccount(user.id, db_row.get("beans"))
		self.account_cache[user.id] = balance_object

		return balance_object

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
	@commands.cooldown(5, 180, commands.BucketType.user)
	async def toss(self, ctx, amount: int = None):
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

	@toss.error
	async def toss_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			msg = "Wow You are doing that so often! \n Wait for: {:.f}s".format(error.retry_after)
			
			embed=discord.Embed(title="Wait for a second!!", description=f"{msg}", color = ctx.author.color)    
			embed.set_thumbnail(url="http://cdn.onlinewebfonts.com/svg/img_571830.png")
			await ctx.send(embed=embed)
		else:
			raise error

	@commands.command()
	async def shop(ctx):
		shop = [
			{"name":"GAM Mug","price":100,"description":"A Mug for hot ones"},
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
	async def set_balance(self, ctx, amount:int):
		account = await self.get_user_balance(ctx.message.author)
		account.set(amount)
		await ctx.send(f"You have now have {account.balance} beans in the bank")

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