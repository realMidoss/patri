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

bot.run('NzQwOTQ1MDE3MDQ0MDc0NTcx.XywY0g.GRWZShHUoqP9KS6JfxVfAOve_34')