# patri
# Patri Bot

import discord
from discord.ext import commands
import datetime

from urllib import parse, request
import re

bot = commands.Bot(command_prefix='.', description="This is a useless Bot", help_command=None)

#Text Commands

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sa(ctx):
    await ctx.send('as')

@bot.command()
async def waifu(ctx):
   await ctx.send('ewww degenerete')

@bot.command()
async def howtobecomehappy(ctx):
    await ctx.send('be happy')

#Embed Commands

@bot.command()
async def lewds(ctx):
    embed = discord.Embed(title="You frickin lolicon!", description="I am under age!")
    embed.set_image(url="https://media.tenor.com/images/a1912e38f72c5df9050d931853fafddb/tenor.gif")
    
    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="I am useless", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
   
    await ctx.send(embed=embed)

@bot.command()
async def invade(ctx):
    embed = discord.Embed(title="Für Das Vaterland", description="Über Alles!")
    embed.set_image(url="https://i.hizliresim.com/XRlk5m.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def HeroFighte(ctx):
    
    embed = discord.Embed(title="Dearest of Midoss", descprition="UwU")
    embed.set_image(url="https://i.hizliresim.com/o5HQ7g.jpg")

    await ctx.send(embed=embed)

#Name Based Commands

@bot.command()
async def warn(ctx,user:discord.Member, *, arg): 
    await ctx.send(f"{user.name} has been warned. Reason: {arg}")

@bot.command()
async def marry(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("You need to marry with someone right? Tag that one!")
        return
    if user==ctx.author:
        await ctx.send("You sadly cant marry yourself...")
        return

    embed = discord.Embed(title=f"{ctx.author} marries to {user.name}", description="Ahhh... So cute! I'm blushing")
    embed.set_image(url="https://media.giphy.com/media/13V4HjgAOIhvDq/giphy.gif")

    await ctx.send(embed=embed)

@bot.command()
async def kill(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("You must mention your target")
        return
   
    embed = discord.Embed(title=f"{ctx.author} kills {user.name}", description="Bam Bam Bam")
    embed.set_image(url="https://i.kym-cdn.com/photos/images/original/000/978/568/24f.gif")

    await ctx.send(embed=embed)    

@bot.command()
async def tsun(ctx):
    
    embed = discord.Embed(title=f"{ctx.author} says: Tsun Tsun Hantsun!", description="Hans is a tsundere")
    embed.set_image(url="https://en.1jux.net/scale_images/456704_b.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def bruh(ctx):
    
    embed = discord.Embed(title=f"{ctx.author} thinks its a bro moment", description="Bro moment is such a moment;")
    embed.set_image(url="https://i.ytimg.com/vi/ZF57zsOWdB0/maxresdefault.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def declarecommunism(ctx):

    embed = discord.Embed(title=f"Stalin would be proud of you comrade {ctx.author}", description="For The Soviet Union!")
    embed.set_image(url="https://media2.giphy.com/media/RMrNQ0HszuxzmvdBdw/giphy.gif")

    await ctx.send(embed=embed)

@bot.command()
async def hug(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("You can't hug air. Tag our lucky boy UwU")
        return
    if user==ctx.author:
        await ctx.send("You cant hug yourself. but your left hand is avaible")
        return
    
    embed = discord.Embed(title=f"{ctx.author} hugs {user.name}", description="Ain't this cute? I envy them...")
    embed.set_image(url="https://data.whicdn.com/images/125740919/original.gif")

    await ctx.send(embed=embed)

@bot.command()
async def hack(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("Target practice? Tag someone!")
        return
   
    embed = discord.Embed(title=f"{ctx.author} hacks {user.name}", description="Damn man homework folder looks kinda sus...")
    embed.set_image(url="https://i.pinimg.com/originals/62/c9/3a/62c93a4cf6462f54fdea6d735d927f9c.gif")    

    await ctx.send(embed=embed)

@bot.command()
async def bully(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("ummm... Ever heard of mentioning other users?")
        return
    if user==ctx.author:
        await ctx.send("Why would you want to bully yourself? Jut look at the mirror")
        return

    embed = discord.Embed(title=f"{ctx.author} bullies {user.name}")
    embed.set_image(url="https://i.pinimg.com/736x/73/08/39/730839953404c1d46a158f12c5c4f78f.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def suck(ctx):

    embed = discord.Embed(title=f"{ctx.author} sucks", description="no not like that you perverted!")
    embed.set_image(url="https://cdn.discordapp.com/attachments/757701650537250957/780183991474454528/popsicleporn.gif")

    await ctx.send(embed=embed)

@bot.command()
async def çay(ctx):

    embed = discord.Embed(title=f"{ctx.author} made tea and grabs a glass of it. Anyone else wants?", description="tea is great")
    embed.set_image(url="https://i.pinimg.com/originals/fd/35/6b/fd356b3bf3fe3a3839efa654aaf52d61.gif")

    await ctx.send(embed=embed)

#bot events

@bot.event
async def on_ready():
    print('I am ready sire')

#help command

@bot.group(invoke_without_command=True)
async def help(ctx):

    embed = discord.Embed(title="Patri Bot", description="A bot made for fun")
    embed.set_thumbnail(url="https://assets.stickpng.com/images/5cb78f9c7ff3656569c8cec2.png")
    
    embed.add_field(name="help", value="you used it already, didnt ya?", inline=False)
    embed.add_field(name="Text based commands", value="howtobecomehappy, sa, ping")
    embed.add_field(name="Fun Commands", value="bruh, bully, declarecommunism, hack, hug, invade, kill, lewds, marry, suck, tsun, waifu, warn, çay")
    embed.add_field(name="Important Commands", value="info, HeroFightie")
    
    await ctx.send(embed=embed)
bot.run('Token')
