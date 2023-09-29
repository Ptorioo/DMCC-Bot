from config import *
from scraper import Scraper

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='songinfo',
        aliases=['si'],
        help=''
    )
    async def songinfo(self, ctx, *args):
        arg = " ".join(args)
        if arg:
            sc = Scraper()
            await ctx.send("Initialized Scraper...")
            info = await sc.scrapeInfo(ctx, arg)

            messages = []
            async for message in ctx.channel.history():
                if message.author == self.bot.user:
                    messages.append(message)
                if len(messages) >= 4:
                    break
            await ctx.channel.delete_messages(messages)

            if info is not None:
                embed = discord.Embed(
                    title="Search Result",
                    description=info[0],
                    colour=0x00FF00
                )
                embed.add_field(
                    name="Artist: ",
                    value=f"{info[1]}",
                    inline=False,
                )
                embed.add_field(
                    name="Key: ",
                    value=f"{info[2]}",
                    inline=False,
                )
                embed.add_field(
                    name="BPM: ",
                    value=f"{info[3]}",
                    inline=False,
                )
                embed.add_field(
                    name="Duration: ",
                    value=f"{info[4]}",
                    inline=False,
                )
                embed.set_footer(text=f"Search requested by: {str(ctx.author)}", icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
            
            else:
                await ctx.send("Song information not found.")
        else:
            await ctx.send("Song information not found.")

async def setup(bot):
    await bot.add_cog(Search(bot))