from config import *

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *arg):
        if len(arg) == 0:
            response = get_response("help")
            await send_response(ctx, response, True)
        elif arg[0] == "music":
            response = get_response("help-music")
            await send_response(ctx, response, True)
        elif arg[0] == "search":
            response = get_response("help-search")
            await send_response(ctx, response, True)
        else:
            return

async def setup(bot):
    bot.remove_command("help")
    await bot.add_cog(Help(bot))

async def send_response(ctx, response, isEmbed):
    if not ctx.guild:
        return
    else:
        if isEmbed:
            await ctx.send(embed=response)
        else:
            await ctx.send(response)

def get_response(arg):
    match arg:
        case "help":
            embed = discord.Embed(
                title="Welcome to DMCC Bot!",
                description="I am a multi-purpose bot created by @lemniscape. \n Find out more about me by using the subcategory help commands listed below!",
                color=0x00FF00,
            )
            embed.add_field(
                name="Music",
                value="`!help music` info about the music commands",
                inline=False,
            )
            embed.add_field(
                name='Search',
                value='`!help search` info about the search engine',
                inline=False
            )
            embed.set_footer(text="Feel free to give me feedback!")
            return embed
        
        case "help-music":
            embed = discord.Embed(title="Music", description="", color=0x00FF00)
            embed.add_field(
                name="Clear",
                value="`!clear`, `!c` clear the current queue",
                inline=False,
            )
            embed.add_field(
                name="Join", value="`!join` join the voice channel", inline=False
            )
            embed.add_field(
                name="Leave",
                value="`!leave`, `!dc`, `!disconnect` disconnect from the current voice channel",
                inline=False,
            )
            embed.add_field(
                name="Pause",
                value="`!pause`, `!stop` pause the current queue",
                inline=False,
            )
            embed.add_field(
                name="Play",
                value="`!play`,`!p` play the song given an url or search keyword \n`!nowplaying`,`!np` show which song is playing in the voice channel",
                inline=False,
            )
            embed.add_field(
                name="Queue",
                value="`!queue`, `!q` show the current queue",
                inline=False,
            )
            embed.add_field(
                name="Resume",
                value="`!resume`, `!r` resume the current queue",
                inline=False,
            )
            embed.add_field(
                name="Skip", value="`!skip`, `!s` skip the current song", inline=False
            )
            embed.set_footer(text="Feel free to give me feedback!")
            return embed
        
        case "help-search":
            embed = discord.Embed(title="Search", description="", color=0x00FF00)
            embed.add_field(
                name="Song Info",
                value="`!songinfo`, `!si` search for the general info about the song",
                inline=False,
            )
            embed.add_field(
                name="MIDI Download",
                value="`!midi`, `!mid` search for MIDI file of the song",
                inline=False,
            )
            embed.set_footer(text="Feel free to give me feedback!")
            return embed
        
        case _:
            return
