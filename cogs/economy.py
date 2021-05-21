import discord
from discord.ext import commands
import random
import asyncio
import json

class economyCog(commands.Cog, name="Economy"):
    def _init_(self, bot):self.bot = bot

amounts = {}

@bot.event
async def on_ready():
    global amounts
    try:
        with open('amounts.json') as f:
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}

@bot.command(pass_context=True)
async def balance(ctx):
    id = str(ctx.message.author.id)
    if id in amounts:
        await ctx.send("You have {} beans in the bank".format(amounts[id]))
    else:
        await ctx.send("You do not have an account. Create one with register command")

@bot.command(pass_context=True)
async def register(ctx):
    id = str(ctx.message.author.id)
    if id not in amounts:
        amounts[id] = 100
        await ctx.send("You are now registered")
        _save()
    else:
        await ctx.send("You already have an account")

@bot.command(pass_context=True)
async def transfer(ctx, amount: int, other: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    if primary_id not in amounts:
        await ctx.send("You do not have an account")
    elif other_id not in amounts:
        await ctx.send("The other party does not have an account")
    elif amounts[primary_id] < amount:
        await ctx.send("You cannot afford this transaction")
    else:
        amounts[primary_id] -= amount
        amounts[other_id] += amount
        await ctx.send("Transaction complete")
    _save()

def _save():
    with open('amounts.json', 'w') as f:
        json.dump(amounts, f)

@bot.command()
async def save():
    _save()

@bot.command()
@commands.cooldown(1, 43200, commands.BucketType.user)
async def work(ctx):

    earned = random.randint(30, 170) 

    id = str(ctx.message.author.id)
    if id not in amounts:
        await ctx.send("You do not have an account. So we can not pay u")   
    else:
        amounts[id] += earned 
        
        embed=discord.Embed(title="Work Work Work!", description=f"You worked hard and got {earned} beans", color = ctx.author.color)
        embed.set_thumbnail(url="https://freepikpsd.com/wp-content/uploads/2019/10/tin-of-beans-png-transparent-tin-of-beanspng-images-pluspng-png-baked-beans-650_650.png")

        await ctx.send(embed=embed)

    pass

    if id not in amounts:
        work.reset_cooldown(ctx)

    _save()
@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "You can only work once in 12 hours \n Next work will be avaible in: {:.2f}s".format(error.retry_after)
        
        embed=discord.Embed(title="Bro chill!", description=f"{msg}", color = ctx.author.color)    
        embed.set_thumbnail(url="http://cdn.onlinewebfonts.com/svg/img_571830.png")
        await ctx.send(embed=embed)
    else:
        raise error

@bot.command()
@commands.cooldown(5, 180, commands.BucketType.user)
async def toss(ctx, amount: int = None):

    if amount == None:
        await ctx.send("You have to give some beans before playing gamble")
        return
    
    A = amount
    user_id = str(ctx.message.author.id)
    coin = random.randint(-2*A, 2*A)
    
    if user_id not in amounts:
        await ctx.send("You do not have an account. So you can not play")   
        return
    elif amount > amounts[user_id]:
        await ctx.send("You don't have enough beans")
        return

    else:
        
        amounts[user_id] += coin

    if coin > 0:  
        embed=discord.Embed(title="heads or tails!", description=f"You are lucky! You just got {coin} beans", color = ctx.author.color)
        embed.set_thumbnail(url="https://www.pngrepo.com/download/261646/coin-flip.png")
        await ctx.send(embed=embed)
    elif coin <= 0:
        em=discord.Embed(title="heads or tails!", description=f"Ah unlucky... You lost {coin} beans", color = ctx.author.color)
        em.set_thumbnail(url="https://www.pngrepo.com/download/261646/coin-flip.png")
        await ctx.send(embed=em)

    def _save():
        with open('amounts.json', 'w') as f:
            json.dump(amounts, f)

    _save()

@toss.error
async def toss_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Wow You are doing that so often! \n Wait for: {:.2f}s".format(error.retry_after)
        
        embed=discord.Embed(title="Wait for a second!!", description=f"{msg}", color = ctx.author.color)    
        embed.set_thumbnail(url="http://cdn.onlinewebfonts.com/svg/img_571830.png")
        await ctx.send(embed=embed)
    else:
        raise error

@bot.command()
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