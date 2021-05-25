import discord
from discord.ext import commands
import random
import asyncio
import sys
import os
from cogs.Turkish import TRCog
from cogs.sub import subCog
from cogs.em import emCog
from cogs.economy import BeansEconomyCog

# From Heroku's own docs
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    DATABASE_URL = "postgres://postgres:password@127.0.0.1:5432/patridb"

bot = commands.Bot(command_prefix=["patri ", "Patri ","p ","P "], help_command=None, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
bot.add_cog(TRCog(bot))
bot.add_cog(subCog(bot))
bot.add_cog(emCog(bot))
bot.add_cog(BeansEconomyCog(bot, DATABASE_URL))

@bot.event
async def on_ready():
    print("Bot looks to be connected to Discord!")
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
    embed.add_field(name="Economy Commands", value="balance, daily, steal, shop, toss, transfer, work")
    embed.add_field(name="Fun Commands", value="ara, bruh, bonk, bully, declarecommunism, F, hug, invade, kick, kill, kiss, lap, marry, nuke, pat, say, suck, warn, question")
    embed.add_field(name="Useful Commands", value="pfp, ping, poll, info, vote")

# Run the bot with a token specified via the command line or at the environment variable PATRI_DISCORD_TOKEN.
if len(sys.argv) > 1:
    os.environ["PATRI_DISCORD_TOKEN"] = str(sys.argv[1])

bot_token = os.environ.get("PATRI_DISCORD_TOKEN")

if bot_token is None:
    print("Missing a bot token! Please specify a bot token as the first command line argument.")
else:
    print("Attempting to start the bot...")
    bot.run(bot_token)
