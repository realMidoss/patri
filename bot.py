import discord
from discord.ext import commands
import random
import asyncio
import json
from cogs.Turkish import TRCog
from cogs.sub import subCog
from cogs.em import emCog

bot = commands.Bot(command_prefix=["patri ", "Patri ","p ","P "], help_command=None, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))

bot.add_cog(TRCog(bot))
bot.add_cog(subCog(bot))
bot.add_cog(emCog(bot))


@bot.event
async def on_ready():
    game = discord.Game("Patri help")    
    await bot.change_presence(status=discord.Status.idle, activity=game)

#Basic Commands

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! {round(bot.latency * 1000)} ms')

@bot.command()
async def say(ctx, *, arg):
    await ctx.send(f'{arg}')

@bot.command()
async def warn(ctx,user:discord.Member, *, arg): 
    await ctx.send(f"{user.name} has been warned. Reason: {arg}")


@bot.command()
async def nuke(ctx):
    
    yas = '✔️'
    nay = '❌'

    embed = discord.Embed(title="Are you sure that you want to use your nukes?", color = ctx.author.color)
    embed = discord.Embed(title="Do you wish to confirm the launch?", color = ctx.author.color)
    embed.add_field(name=f"ID: {ctx.author.name}", value="Acces approved...")
    embed.set_thumbnail(url=ctx.author.avatar_url)
    message = await ctx.send(embed=embed)

    
    await message.add_reaction(yas)
    await message.add_reaction(nay)
    
    valid_reactions = ['✔️', '❌']
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reactions
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Cancelled...")
    
    if str(reaction.emoji) == yas:
        embed = discord.Embed(title="Code:87453 Activated, Destruction stars...", description=f"{ctx.author.name} used their nukes...", color=discord.Color.dark_red())
        embed.set_image(url="https://i.gifer.com/3Tt5.gif")
        return await ctx.send(embed=embed)
    
    await ctx.send("Progress Abondoned...") 

@bot.command()
async def HeroFighte(ctx):
    
    hero = [
    "https://cdn.discordapp.com/attachments/745035581670817842/796360277952036874/Face.png",
    "https://cdn.discordapp.com/attachments/745035581670817842/796360329549316136/fullbody.png",
    "https://cdn.discordapp.com/attachments/745035581670817842/796360361296658492/65-2.png",
    "https://cdn.discordapp.com/attachments/745035581670817842/796360385849851974/HF_noBG.png",
    "https://cdn.discordapp.com/attachments/745035581670817842/796360480767213568/OCMP7Cosplay.png",
    "https://cdn.discordapp.com/attachments/745035581670817842/796360495552135178/HeroExplains.png",
    "https://cdn.discordapp.com/attachments/745035581670817842/796360544696664064/HeroUnderweardone.png",
    ]


    embed = discord.Embed(title="Dearest of Midoss", descprition="UwU")
    embed.set_image(url=random.choice(hero))

    await ctx.send(embed=embed)

#help command

@bot.group(invoke_without_command=True)
async def help(ctx):

    embed = discord.Embed(title="Patri Bot", description="Basic Fun Bot for GAM \n by Midoss", color = ctx.author.color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/762217890111029268.png?v=1")
    
    embed.add_field(name="help", value="you used it already, didnt ya?", inline=False)
    embed.add_field(name="Economy Commands", value="balance, register, save, shop, toss, transfer, work")
    embed.add_field(name="Fun Commands", value="ara, bruh, bully, declarecommunism, F, hug, invade, kick, kill, kiss, lap, marry, nuke, pat, say, suck, warn, question")
    embed.add_field(name="Usefull Commands", value="pfp, ping, poll, info, vote")
    
    await ctx.send(embed=embed)
    
#Ekonomi

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
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):

    earned = random.randint(50, 250) 

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
        msg = "You can only work once every hour \n Next work will be avaible in: {:.2f}s".format(error.retry_after)
        
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
    
@bot.command()
async def add(ctx, amount: int, user: discord.Member):

    ID = 354316211657506827
    user_id = str(user.id)
    
    if ctx.message.author.id == ID:
        amounts[user_id] += amount
        await ctx.send("Transaction complete")
    else:
        await ctx.send('You are not allowed to execute this command!')
    
    def _save():
        with open('amounts.json', 'w') as f:
            json.dump(amounts, f)

    _save()
bot.run('NzQwOTQ1MDE3MDQ0MDc0NTcx.XywY0g.GRWZShHUoqP9KS6JfxVfAOve_34')
