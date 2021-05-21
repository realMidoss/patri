import discord
from discord.ext import commands
from urllib import parse, request
import re
import random
import asyncio

class TRCog(commands.Cog, name="Turkish"):
    def _init_(self, bot):self.bot = bot

    @commands.group(invoke_without_command=True)
    async def yumurtalar(self, ctx):

        embed = discord.Embed(title="Yüce Türk Milletine Armağan olsun", description="Sürpriz Yumurta Komutları")
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/770041004073418822.png?v=1")
        
        embed.add_field(name="yumurtalar", value="Bu menüyü açar", inline=False)
        embed.add_field(name="Ağlama Komutları", value="f35")
        embed.add_field(name="Gır Gır Komutları", value="çay, söv")
        
        await ctx.send(embed=embed)

    @commands.command()
    async def çay(self, ctx):

        embed = discord.Embed(title=f"{ctx.author.name} made tea and grabs a glass of it. Anyone else wants?", description="tea is great", color=discord.Color.red())
        embed.set_image(url="https://i.pinimg.com/originals/fd/35/6b/fd356b3bf3fe3a3839efa654aaf52d61.gif")

        await ctx.send(embed=embed)
    
    @commands.command()
    async def f35(self, ctx):

        embed = discord.Embed(title=f"{ctx.author.name} f35lere bakıyor ve ağlıyor")
        embed.set_image(url="https://img.piri.net/mnresize/840/-/resim/imagecrop/2019/12/10/11/45/resized_b3d5f-f1d85093mansetc.jpg")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 200, commands.BucketType.user)
    async def söv(self, ctx, user:discord.Member = None):

        kufurler = [
        "Senin ben yedi ceddini dere başında sikeyim",
        "Yedi ceddinin adet suyuna ekmek banayım ",
        "Senin gibilerin hak ettiği tek yer sikimin ucudur ama kendimi boka bulamak istemiyorum",
        "Weeb'in oğlu",
        "Sana açılan ilim irfan yuvalarının menteşelerini sikeyim",
        "Bacına telif hakkı koyayım",
        "Götüne kürek sokayım, çocuklara tahteravalli yapayım",
        "Ebeni kaçırıp ormana atayım, sırtına bal sürüp ayılara siktireyim",
        "Seni müjdeleyen doktoru sikiyim",
        "Halimize şükretmeliyiz. Senin gibi olmak da vardı",
        "Senin kârını sikerim",
        "Karının karnına Ermeni yarrağı saplayayım",
        "Senin amını yeni kategori açana dek sikeyim",
        "Ebeni uzaya göndereyim, yeni nesiller üretene dek uzaylılara siktireyim",
        "Seni ben götünden omuriliğine kadar yararım, orospunun döletinin müjdelediği seni",
        "Ebeni çarprazlayayım."
        ]
        
        if user is None:
            await ctx.send("kime söveyim amk?")
            return
        
        if user==ctx.author:
            await ctx.send("Kendine saygın olsun biraz.")
            return
        
        if(user.bot):
            await ctx.send(f'{ctx.author.name}, Seni yoğurtlar, çatır çutur sikerim çocuk.')
            return

        await ctx.send(f'{user.name}, {random.choice(kufurler)}')

    @söv.error
    async def toss_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "Bekle bakalım! \n Sonraki küfre: {:.2f}s".format(error.retry_after)
            
            embed=discord.Embed(title="Sal AMK", description=f"{msg}", color = ctx.author.color)    
            embed.set_thumbnail(url="https://www.pngkit.com/png/full/603-6030012_open-11-11-clock-png.png")
            await ctx.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(TRCog(bot))
    print('Türkçe Yüklendi')