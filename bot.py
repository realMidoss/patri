import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re
import random
import asyncio

bot = commands.Bot(command_prefix=["patri ", "Patri ","p ","P "], help_command=None, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))

#Poll Komutu 

@bot.command()
async def poll(ctx, *, arg):
    
    yas = '✔️' 
    idk = '♻️'
    nay = '❌'
    
    embed = discord.Embed(title=f"{ctx.author.name} asks:", description=f"{arg}", color=ctx.author.color)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    message = await ctx.send(embed=embed)
    
    await message.add_reaction(yas)
    await message.add_reaction(idk)
    await message.add_reaction(nay)


#bot events

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="patri help"))
    print('I am redy')

#Text Commands

@bot.command(pass_context=True)
async def question(ctx, *, arg):
    variable = [
        "sure",
        "yes",
        "hell no",
        "Maybe",
        "Mayhabs",
        "Why not?",
        "IDK",
        "How the fuck I can know?",]
    await ctx.send(random.choice(variable))

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! {round(bot.latency * 1000)} ms')

@bot.command()
async def say(ctx, *, arg):
    await ctx.send(f'{arg}')

#Embed Commands

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="I am useless", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
   
    await ctx.send(embed=embed)

@bot.command()
async def invade(ctx):
    embed = discord.Embed(title="Für Das Vaterland", description="Über Alles!", color=discord.Color.red())
    embed.set_image(url="https://i.hizliresim.com/XRlk5m.jpg")

    await ctx.send(embed=embed)

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
    
    marriage = [
    "https://media.giphy.com/media/13V4HjgAOIhvDq/giphy.gif",
    "https://data.whicdn.com/images/282240022/original.gif",
    "https://pa1.narvii.com/6220/724eef7024976360a3d683bed7531b951fefffb0_00.gif",
    "https://i.pinimg.com/originals/0e/5a/e8/0e5ae8c0c07c847e1f8c4d1c8665872f.gif",
    "https://pa1.narvii.com/6505/af2b8c242ffdb5300dd1bf83a2587e44b1d12298_00.gif",]

    embed = discord.Embed(title=f"{ctx.author.name} marries to {user.name}", description="Ahhh... So cute! I'm blushing", color=ctx.author.color)
    embed.set_image(url=random.choice(marriage))

    await ctx.send(embed=embed)

@bot.command()
async def kill(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("You must mention your target")
        return

    if user==ctx.author:
        
        intihar = [
        "https://data.whicdn.com/images/89750923/original.gif",
        "https://64.media.tumblr.com/130a00d77bd535456e4518cf1f9397f9/tumblr_pdf9aaSUmM1xci9v9o2_500.gif",
        "https://data.whicdn.com/images/251664843/original.gif",]

        embed = discord.Embed(title=f"{ctx.author.name} commited suicide ", description="F")
        embed.set_image(url=random.choice(intihar))  
        
        await ctx.send(embed=embed)

        return
    
    killv = [
    "https://i.kym-cdn.com/photos/images/original/000/978/568/24f.gif",
    "https://i.pinimg.com/originals/d4/bb/e2/d4bbe21cfe5993e13173c4692db757d0.gif",
    "https://i.kym-cdn.com/photos/images/newsfeed/000/637/941/20b.gif",] 

    embed = discord.Embed(title=f"{ctx.author.name} kills {user.name}", description="Bam Bam Bam", color=discord.Color.dark_red())
    embed.set_image(url=random.choice(killv)) 

    await ctx.send(embed=embed)    

@bot.command()
async def tsun(ctx):
    
    user = await bot.fetch_user(291094866778259457)
    embed = discord.Embed(title=f"{ctx.author.name} thinks {user.name} is a tsundere!", description="Tsun tsun Hantsun!", color=discord.Color.magenta())
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def bruh(ctx):
    
    embed = discord.Embed(title=f"{ctx.author.name} thinks its a bro moment", description="Bro moment is such a moment;", color=discord.Color.darker_gray())
    embed.set_image(url="https://i.ytimg.com/vi/ZF57zsOWdB0/maxresdefault.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def declarecommunism(ctx):

    komün = [
    "https://media2.giphy.com/media/RMrNQ0HszuxzmvdBdw/giphy.gif",
    "https://31.media.tumblr.com/1c34ba04ed84aa28afa59511a1b4f99c/tumblr_inline_np4407k8KS1rfowug_500.gif",
    "https://pa1.narvii.com/7147/2d29995dcaf867d19fc76e00a2077bb93c2429fdr1-380-335_hq.gif",
    ]
    embed = discord.Embed(title=f"Stalin would be proud of you comrade {ctx.author}", description="For The Soviet Union!", color=discord.Color.dark_red())
    embed.set_image(url=random.choice(komün)) 

    await ctx.send(embed=embed)

@bot.command()
async def hug(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("You can't hug air. Tag our lucky boy UwU")
        return
    if user==ctx.author:
        await ctx.send("You cant hug yourself. but your left hand is available")
        return
    
    hugv = [
    "https://data.whicdn.com/images/125740919/original.gif",
    "https://i.pinimg.com/originals/f2/80/5f/f2805f274471676c96aff2bc9fbedd70.gif",
    "https://media2.giphy.com/media/l2QDM9Jnim1YVILXa/source.gif",
    ]

    embed = discord.Embed(title=f"{ctx.author.name} hugs {user.name}", description="Ain't this cute? I envy them...", color = ctx.author.color)
    embed.set_image(url=random.choice(hugv)) 

    await ctx.send(embed=embed)

@bot.command()
async def bully(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("ummm... Ever heard of mentioning other users?")
        return
    if user==ctx.author:
        await ctx.send("Why would you want to bully yourself? Just look at the mirror")
        return

    embed = discord.Embed(title=f"{ctx.author.name} bullies {user.name}", color=discord.Color.blue())
    embed.set_image(url="https://i.pinimg.com/736x/73/08/39/730839953404c1d46a158f12c5c4f78f.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("Kiss what? More likely who? :kekw: Will you kiss air, you poor thing?")
        return
    if user==ctx.author:
        await ctx.send("OMG did you just try to kiss yourself :kekw:")
        return

    öp = [
    "https://media3.giphy.com/media/12VXIxKaIEarL2/giphy.gif",
    "https://37.media.tumblr.com/7bbfd33feb6d790bb656779a05ee99da/tumblr_mtigwpZmhh1si4l9vo1_500.gif",
    "https://data.whicdn.com/images/239776661/original.gif",
    "https://i.pinimg.com/originals/f8/e8/8e/f8e88eccd2737d5805d645a85d1dbc0f.gif",
    "https://i.pinimg.com/originals/21/82/d8/2182d81bc459732fdf9bf94d1dd068c4.gif",
    ]

    embed = discord.Embed(title=f"{ctx.author.name} kissed {user.name}...", description="Ahh young love...", color=discord.Color.magenta())
    embed.set_image(url=random.choice(öp)) 

    await ctx.send(embed=embed)

@bot.command()
async def suck(ctx):

    embed = discord.Embed(title=f"{ctx.author.name} sucks", description="no not like that you perverted!")
    embed.set_image(url="https://cdn.discordapp.com/attachments/757701650537250957/780183991474454528/popsicleporn.gif")

    await ctx.send(embed=embed)

@bot.command()
async def çay(ctx):

    embed = discord.Embed(title=f"{ctx.author.name} made tea and grabs a glass of it. Anyone else wants?", description="tea is great", color=discord.Color.red())
    embed.set_image(url="https://i.pinimg.com/originals/fd/35/6b/fd356b3bf3fe3a3839efa654aaf52d61.gif")

    await ctx.send(embed=embed)

@bot.command()
async def F(ctx):

    Fv = [
    "https://i.kym-cdn.com/entries/icons/mobile/000/017/039/pressf.jpg",
    "https://i.pinimg.com/originals/4c/c5/3a/4cc53a5ae71234a0fd79998a8d2a802f.png",
    "https://cdn.ebaumsworld.com/thumbs/2019/02/14/060133/85886769/meme-fixed.jpg"
    ]

    embed = discord.Embed(title="F", color = ctx.author.color)
    embed.set_image(url=random.choice(Fv))

    await ctx.send(embed=embed)


@bot.command()
async def pat(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("Pat what? Mention someone")
        return
    
    if user==ctx.author:
        embed = discord.Embed(title=f"{ctx.author.name} pats theirselves... It's just sad")
        embed.set_image(url="https://pa1.narvii.com/6400/6a38438c39e60789ac39cfd7340acd868baeac90_00.gif")
        await ctx.send(embed=embed)
        return

    patv = [
    "https://i.imgur.com/LUChfFZ.gif",
    "https://66.media.tumblr.com/d743a5e5ecc65be5cb6ac8de7978fb22/tumblr_pfyit1ofSu1th206io1_500.gif",
    "https://i.imgur.com/LUypjw3.gif",
    "https://i.pinimg.com/originals/ec/b8/7f/ecb87fb2827a022884d5165046f6608a.gif",
    "https://thumbs.gfycat.com/ImpurePleasantArthropods-small.gif",
    ]

    embed = discord.Embed(title=f"{ctx.author.name} pats, {user.name}", description="pat pat", color=discord.Color.gold())
    embed.set_image(url=random.choice(patv))

    await ctx.send(embed=embed)

@bot.command()
async def lappillow(ctx,user:discord.Member = None):
    
    if user is None:
        await ctx.send("You need to give lap pillows. That's cute but mention someone")
        return
    
    if user==ctx.author:
        await ctx.send("That's a bro moment. But you cant lie on your own lap unless you broke your neck...")
        return   
    
    yastik = [
    "https://i.hizliresim.com/pgTnCN.gif",
    "https://media.tenor.com/images/6eb51ecba07ba236ab717ca1fa3a02a0/tenor.gif",
    "https://media.tenor.com/images/f6053a70c19ac74045aae1cfc9c85e78/tenor.gif",
    "https://cdn.awwni.me/t3m5.gif"
    ]

    embed = discord.Embed(title=f"{user.name} gets a cute lap pillow from {ctx.author.name}", description="That's so lovely!", color = ctx.author.color)
    embed.set_image(url=random.choice(yastik))

    await ctx.send(embed=embed)

@bot.command()
async def pogchamp(ctx,user:discord.Member = None):
    if user is None:
        await ctx.send("Tag someone stupid!")
        return
    
    if user==ctx.author:
        await ctx.send("Ara? Do you wanna be your own pogchamp? That's cute")
        return  

    embed = discord.Embed(title=f"Fine! Guess your my little pogchamp... Come here {user.name}", description="I'm blusing", color = ctx.author.color)
    embed.set_image(url="https://i.ytimg.com/vi/7awd-y_DTQY/maxresdefault.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def nuke(ctx):
    
    yas = '✔️'
    nay = '❌'
    
    embed = discord.Embed(title="Do you wish to confirm the launch?", color = ctx.author.color)
    embed.add_field(name=f"ID: {ctx.author.name}", value="Access approved...")
    embed.set_thumbnail(url=ctx.author.avatar_url)
    message = await ctx.send(embed=embed)
    
    
    await message.add_reaction(yas)
    await message.add_reaction(nay)
    
    valid_reactions = ['✔️', '❌']
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reactions
    try:
        reaction = await bot.wait_for('reaction_add', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Progress Abondoned...")
    
    if str(reaction.emoji) == yas:
        embed = discord.Embed(title="Code:87453 Activated, Destruction stars...", description=f"{ctx.author.name} used their nukes...", color=discord.Color.dark_red())
        embed.set_image(url="https://i.gifer.com/3Tt5.gif")
        return await ctx.send(embed=embed)
    
    embed = discord.Embed(title="Cancelled", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def ara(ctx):
    
    arav = [
    "https://i.pinimg.com/originals/14/16/8e/14168e97f35efe70cbdb386122e1b5e9.gif",
    "https://i.pinimg.com/originals/11/90/66/119066a6751819f2d20e4760a2ad4277.gif",
    "https://64.media.tumblr.com/6f917421b530790905865539cb919dad/tumblr_p1o3qcsLqO1wmel88o3_500.gifv",
    "https://i.hizliresim.com/MQaeNF.gif",
    "https://media.tenor.com/images/7ea76f356b64ec0fbb47341e872f7ea2/tenor.gif",
    "https://64.media.tumblr.com/2086b091452d87e5b3322923b9bb2256/tumblr_px6l0gh5ZH1vip2zbo2_500.gifv",
    ]

    embed = discord.Embed(title=f"{ctx.author.name} ara ara's...", description="Kinda cute", color=discord.Color.red())
    embed.set_image(url=random.choice(arav))
    
    await ctx.send(embed=embed)
      
#Ekonomi Komutları 



#help command

@bot.group(invoke_without_command=True)
async def help(ctx):

    embed = discord.Embed(title="Patri Bot", description="Basic Fun Bot for GAM \n by Midoss", color = ctx.author.color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/762217890111029268.png?v=1")
    
    embed.add_field(name="help", value="you used it already, didnt ya?", inline=False)
    embed.add_field(name="Economy Commands", value="Coming soon...")
    embed.add_field(name="Fun Commands", value="ara, bruh, bully, declarecommunism, F, hug, invade, kill, kiss, lappilow, marry, nuke, pat, pogchamp, say, suck, tsun, warn, question")
    embed.add_field(name="Usefull Commands", value="HeroFighte, ping, poll, info")
    
    await ctx.send(embed=embed)

#easter eggs (Burdan sonrası Türklere hitap etmektedir)

@bot.group(invoke_without_command=True)
async def yumurtalar(ctx):

    embed = discord.Embed(title="Yüce Türk Milletine Armağan olsun", description="Sürpriz Yumurta Komutları")
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/770041004073418822.png?v=1")
    
    embed.add_field(name="yumurtalar", value="Bu menüyü açar", inline=False)
    embed.add_field(name="Ağlama Komutları", value="f35")
    embed.add_field(name="Gır Gır Komutları", value="çay, söv")
    
    await ctx.send(embed=embed)

@bot.command()
async def f35(ctx):

    embed = discord.Embed(title=f"{ctx.author.name} f35lere bakıyor ve ağlıyor")
    embed.set_image(url="https://img.piri.net/mnresize/840/-/resim/imagecrop/2019/12/10/11/45/resized_b3d5f-f1d85093mansetc.jpg")

    await ctx.send(embed=embed)

@bot.command()
async def söv(ctx, user:discord.Member = None):

    kufurler = [
    "Senin ben yedi ceddini dere başında sikeyim",
    "Yedi ceddinin adet suyuna ekmek banayım ",
    "Senin gibilerin hak ettiği tek yer sikimin ucudur ama kendimi boka bulamak istemiyorum",
    "Weeb'in oğlu",
    "Sana açılan ilim irfan yuvalarının menteşelerini sikeyim",
    "Bacına telif hakkı koyayım",
    "Götüne kürek sokayım, çocuklara tahteravalli yapayım",]
    
    if user is None:
        await ctx.send("kime söveyim amk?")
        return

    if user==ctx.author:
        await ctx.send("Kendine saygın olsun biraz.")
        return

    await ctx.send(f'{user.name}, {random.choice(kufurler)}')

bot.run('NzQwOTQ1MDE3MDQ0MDc0NTcx.XywY0g.GRWZShHUoqP9KS6JfxVfAOve_34')
