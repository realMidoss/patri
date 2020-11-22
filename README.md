# patri
Patri Bot

import discord
from discord.ext import commands
import datetime

from urllib import parse, request
import re

bot = commands.Bot(command_prefix='.', description="This is a useless Bot")

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
async def warn(ctx,user:discord.User, *, arg):
    await ctx.send(f"{user.name} has been warned. Reason: {arg}")

@bot.command()
async def marry(ctx,user:discord.Member):

    embed = discord.Embed(title=f"{ctx.author} marries to {user.name}", description="Ahhh... So cute! I'm blushing")
    embed.set_image(url="https://media.giphy.com/media/13V4HjgAOIhvDq/giphy.gif")

    await ctx.send(embed=embed)

@bot.command()
async def kill(ctx,user:discord.Member):

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
async def hug(ctx,user:discord.Member):
    
    embed = discord.Embed(title=f"{ctx.author} hugs {user.name}", description="Ain't this cute? I envy them...")
    embed.set_image(url="https://data.whicdn.com/images/125740919/original.gif")

    await ctx.send(embed=embed)

@bot.command()
async def hack(ctx,user:discord.Member):

    embed = discord.Embed(title=f"{ctx.author} hacks {user.name}", description="Damn man homework folder looks kinda sus...")
    embed.set_image(url="https://i.pinimg.com/originals/62/c9/3a/62c93a4cf6462f54fdea6d735d927f9c.gif")    

    await ctx.send(embed=embed)


#bot events

@bot.event
async def on_ready():
    print('I am ready sire')

bot.run('Token')
