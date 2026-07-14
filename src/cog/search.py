from config import *
from scraper import Scraper

@app_commands.guilds(*sync_guilds)
class Search(commands.GroupCog, name="search", description = "searching for song"):
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

    @app_commands.command(
        name="songinfo",
        description="search for the general info about the song"
    )
    @app_commands.describe(
        name="name of the song, artist, etc..."
    )
    async def songinfo(self, ctx, name:str):
        if not ctx.guild:
            return

        arg = " ".join(name)

        if arg:
            sc = Scraper()
            info, respond = await sc.scrapeInfo(ctx, arg)

            #await self.deleteDebugInfo(ctx)

            if len(info) > 1:
                embed = discord.Embed(
                    title="Title", description=info[1], colour=0x00FF00
                )
                embed.add_field(
                    name="Artist: ",
                    value=f"{info[0]}",
                    inline=False,
                )
                embed.add_field(
                    name="Key: ",
                    value=f"{info[3]}",
                    inline=False,
                )
                embed.add_field(
                    name="BPM: ",
                    value=f"{info[4]}",
                    inline=False,
                )
                embed.add_field(
                    name="Duration: ",
                    value=f"{info[5]}",
                    inline=False,
                )
                embed.add_field(
                    name="Loudness: ",
                    value=f"{info[6]}",
                    inline=False,
                )
                embed.set_thumbnail(url=info[2])
                embed.set_footer(
                    text=f"Search requested by: {str(ctx.user)}",
                    icon_url=ctx.user.avatar,
                )
                await respond.edit(content="",embed=embed)

            else:
                await ctx.followup.send(
                    f"Song information not found, or there are multiple search results. Error code: {info[0]}"
                )
        else:
            await ctx.followup.send("Song information not found.")

    @app_commands.command(
        name="midi",
        description="search for the general info about the song"
    )
    @app_commands.describe(
        name="name of the song, artist, etc..."
    )
    async def midi(self, ctx, name:str):
        if not ctx.guild:
            return

        arg = " ".join(name)

        if arg:
            sc = Scraper()
            result = await sc.scrapeMIDI(ctx, arg)

            await self.deleteDebugInfo(ctx)

            if len(result) > 1:
                filename = f"{result[0]} - {result[1]}.mid"
                await ctx.followup.send(file=discord.File(fp=result[-1], filename=filename))
            else:
                await ctx.followup.send(
                    f"MIDI information not found, or there are multiple search results. Error code: {result[0]}"
                )
        else:
            await ctx.followup.send("MIDI information not found.")

    @app_commands.command(
        name="lyrics",
        description="search for lyrics of the song"
    )
    @app_commands.describe(
        name="name of the song, artist, etc..."
    )
    async def lyrics(self, ctx, name:str):
        if not ctx.guild:
            return

        arg = " ".join(name)

        if arg:
            sc = Scraper()
            result = await sc.scrapeLyrics(ctx, arg)

            await self.deleteDebugInfo(ctx)

            if len(result) > 1:
                embed = discord.Embed(
                    title="Title",
                    description=f"{result[0]} - {result[1]}",
                    colour=0x00FF00,
                )

                for i in range(3, len(result)):
                    if i == 3:
                        name = "Lyrics"
                    else:
                        name = ""
                    embed.add_field(
                        name=name,
                        value=f"{result[i]}",
                        inline=False,
                    )

                embed.set_thumbnail(url=result[2])
                embed.set_footer(
                    text=f"Search requested by: {str(ctx.user)}",
                    icon_url=ctx.user.avatar,
                )
                await ctx.followup.send(embed=embed)
            else:
                await ctx.followup.send(f"Lyrics information not found. Error code: {result[0]}")
        else:
            await ctx.followup.send("Lyrics information not found.")


async def setup(bot):
    await bot.add_cog(Search(bot))
