from config import *
from scraper import Scraper

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def deleteDebugInfo(self, ctx):
        messages = []
        async for message in ctx.channel.history():
            if message.author == self.bot.user:
                messages.append(message)
            if len(messages) >= 2:
                break
        await ctx.channel.delete_messages(messages)

    @commands.command(
        name='songinfo',
        aliases=['si'],
        help=''
    )
    async def songinfo(self, ctx, *args):
        if not ctx.guild:
            return
        
        arg = " ".join(args)

        if arg:
            sc = Scraper()
            info = await sc.scrapeInfo(ctx, arg)

            await self.deleteDebugInfo(ctx)

            if len(info) > 1:
                embed = discord.Embed(
                    title="Title",
                    description=info[1],
                    colour=0x00FF00
                )
                embed.add_field(
                    name="Artist: ",
                    value=f"{info[0]}",
                    inline=False,
                )
                embed.add_field(
                    name="Key: ",
                    value=f"{info[8]}",
                    inline=False,
                )
                embed.add_field(
                    name="BPM: ",
                    value=f"{info[9]}",
                    inline=False,
                )
                embed.add_field(
                    name="Duration: ",
                    value=f"{info[13]}",
                    inline=False,
                )
                embed.set_thumbnail(url='https://www.cprato.com' + info[5])
                embed.set_footer(text=f"Search requested by: {str(ctx.author)}", icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
            
            else:
                await ctx.send(f"Song information not found, or there are multiple search results. Error code: {info[0]}")
        else:
            await ctx.send("Song information not found.")
    
    @commands.command(
        name='midi',
        aliases=['mid'],
        help=''
    )
    async def midi(self, ctx, *args):
        if not ctx.guild:
            return

        arg = " ".join(args)

        if arg:
            sc = Scraper()
            result = await sc.scrapeMIDI(ctx, arg)

            await self.deleteDebugInfo(ctx)

            if len(result) > 1:
                filename = f'{result[0]} - {result[1]}.mid'
                await ctx.send(file=discord.File(fp=result[-1], filename=filename))
            else:
                await ctx.send(f"MIDI information not found, or there are multiple search results. Error code: {result[0]}")
        else:
            await ctx.send("MIDI information not found.")
    
    @commands.command(
        name='lyrics',
        aliases=['lyr'],
        help=''
    )
    async def lyrics(self, ctx, *args):
        if not ctx.guild:
            return
        
        arg = " ".join(args)

        if arg:
            sc = Scraper()
            result = await sc.scrapeLyrics(ctx, arg)

            await self.deleteDebugInfo(ctx)

            if len(result) > 1:
                embed = discord.Embed(
                    title='Title',
                    description=f'{result[0]} - {result[1]}',
                    colour=0x00FF00
                )

                for i in range(3, len(result)):
                    if i == 3:
                        name = 'Lyrics'
                    else:
                        name = ''
                    embed.add_field(
                        name=name,
                        value=f'{result[i]}',
                        inline=False,
                    )
                
                embed.set_thumbnail(url=result[2])
                embed.set_footer(text=f"Search requested by: {str(ctx.author)}", icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Lyrics information not found. Error code: {result[0]}")
        else:
            await ctx.send("Lyrics information not found.")

async def setup(bot):
    await bot.add_cog(Search(bot))