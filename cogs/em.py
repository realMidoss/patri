import discord
from discord.ext import commands
import random
import asyncio

class emCog(commands.Cog, name="Sub"):
    def _init_(self, bot):self.bot = bot


    @commands.command()
    async def invade(self, ctx):
        embed = discord.Embed(title="Für Das Vaterland", description="Über Alles!", color=discord.Color.red())
        embed.set_image(url="https://i.hizliresim.com/XRlk5m.jpg")

        await ctx.send(embed=embed)

    @commands.command()
    async def marry(self, ctx,user:discord.Member = None):
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

    @commands.command()
    async def kill(self, ctx,user:discord.Member = None):
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

    @commands.command()
    async def bruh(self, ctx):
        
        embed = discord.Embed(title=f"{ctx.author.name} thinks its a bro moment", description="Bro moment is such a moment;", color=discord.Color.darker_gray())
        embed.set_image(url="https://i.ytimg.com/vi/ZF57zsOWdB0/maxresdefault.jpg")

        await ctx.send(embed=embed)

    @commands.command()
    async def declarecommunism(self, ctx):

        komün = [
        "https://media2.giphy.com/media/RMrNQ0HszuxzmvdBdw/giphy.gif",
        "https://31.media.tumblr.com/1c34ba04ed84aa28afa59511a1b4f99c/tumblr_inline_np4407k8KS1rfowug_500.gif",
        "https://pa1.narvii.com/7147/2d29995dcaf867d19fc76e00a2077bb93c2429fdr1-380-335_hq.gif",
        ]
        embed = discord.Embed(title=f"Stalin would be proud of you comrade {ctx.author}", description="For The Soviet Union!", color=discord.Color.dark_red())
        embed.set_image(url=random.choice(komün)) 

        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx,user:discord.Member = None):
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

    @commands.command()
    async def bully(self, ctx,user:discord.Member = None):
        if user is None:
            await ctx.send("ummm... Ever heard of mentioning other users?")
            return
        if user==ctx.author:
            await ctx.send("Why would you want to bully yourself? Just look at the mirror")
            return

        embed = discord.Embed(title=f"{ctx.author.name} bullies {user.name}", color=discord.Color.blue())
        embed.set_image(url="https://i.pinimg.com/736x/73/08/39/730839953404c1d46a158f12c5c4f78f.jpg")

        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx,user:discord.Member = None):
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

    @commands.command()
    async def suck(self, ctx):

        embed = discord.Embed(title=f"{ctx.author.name} sucks", description="no not like that you perverted!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/757701650537250957/780183991474454528/popsicleporn.gif")

        await ctx.send(embed=embed)

    @commands.command()
    async def F(ctx):

        Fv = [
        "https://i.kym-cdn.com/entries/icons/mobile/000/017/039/pressf.jpg",
        "https://i.pinimg.com/originals/4c/c5/3a/4cc53a5ae71234a0fd79998a8d2a802f.png",
        "https://cdn.ebaumsworld.com/thumbs/2019/02/14/060133/85886769/meme-fixed.jpg"
        ]

        embed = discord.Embed(title="F", color = ctx.author.color)
        embed.set_image(url=random.choice(Fv))

        await ctx.send(embed=embed)


    @commands.command()
    async def pat(self, ctx,user:discord.Member = None):
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

    @commands.command()
    async def lap(self, ctx,user:discord.Member = None):
        
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

    @commands.command()
    async def ara(self, ctx):
        
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

    @commands.command()
    async def kick(self, ctx,user:discord.Member = None): 

        if user is None:
            await ctx.send("You need to mention the person that you wanted to kick")
            return

        if user==ctx.author:
            await ctx.send("You can not kick yourself. It is not 1984")
            return
            
        embed = discord.Embed(title=f"{user.name} has been kicked", color=discord.Color.dark_red())
        embed.set_image(url="https://media.tenor.com/images/27f16871c55a3376fa4bfdd76ac2ab5c/tenor.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def bonk(self, ctx, user:discord.Member = None):
        if user is None:
            await ctx.send("Mantion someone for god's sake")
            return

        if user==ctx.author:
            await ctx.send("I wouldn't bonk myself")
            return

        bonkv = "https://media1.tenor.com/images/6493bee2be7ae168a5ef7a68cf751868/tenor.gif?itemid=17298755"

        embed = discord.Embed(title=f"{ctx.author.name} Bonks {user.name}", description="Should have hurt", color=discord.Color.red())
        embed.set_image(url=bonkv)


def setup(commands):
    commands.add_cog(emCog(commands))
    print('Embed Commands are ready')