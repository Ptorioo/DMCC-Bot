from config import *


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="Know how to use the bot"
    )
    @app_commands.describe(
        group="the command group you want to know how to use"
    )
    async def help(self, ctx, group:str = ""):
        if not group:
            response = get_response("help")
            await send_response(ctx, response, True)
        elif group == "music":
            response = get_response("help-music")
            await send_response(ctx, response, True)
        elif group == "search":
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
            await ctx.response.send_message(embed=response)
        else:
            await ctx.response.send_message(response)


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
                value="`/help group:music` info about the music commands",
                inline=False,
            )
            embed.add_field(
                name="Search",
                value="`/help group:search` info about the search engine",
                inline=False,
            )
            embed.set_footer(text="Feel free to give me feedback!")
            return embed

        case "help-music":
            embed = discord.Embed(title="Music", description="", color=0x00FF00)
            embed.add_field(
                name="Clear",
                value="`/music clear` clear the current queue",
                inline=False,
            )
            embed.add_field(
                name="/music join", value="`!join` join the voice channel", inline=False
            )
            embed.add_field(
                name="Leave",
                value="`/music leave` disconnect from the current voice channel",
                inline=False,
            )
            embed.add_field(
                name="Pause",
                value="`/music pause` pause the current queue",
                inline=False,
            )
            embed.add_field(
                name="Play",
                value="`/music play` play the song given an url or search keyword \n`/music now_playing` show which song is playing in the voice channel",
                inline=False,
            )
            embed.add_field(
                name="Queue",
                value="`/music queue` show the current queue",
                inline=False,
            )
            embed.add_field(
                name="Resume",
                value="`/music resume` resume the current queue",
                inline=False,
            )
            embed.add_field(
                name="Skip", value="`/music skip` skip the current song", inline=False
            )
            embed.set_footer(text="Feel free to give me feedback!")
            return embed

        case "help-search":
            embed = discord.Embed(title="Search", description="", color=0x00FF00)
            embed.add_field(
                name="Song Info",
                value="`/search songinfo` search for the general info about the song",
                inline=False,
            )
            embed.add_field(
                name="MIDI Download",
                value="`/search midi` search for MIDI file of the song",
                inline=False,
            )
            embed.add_field(
                name="Lyrics Search",
                value="`/search lyrics` search for lyrics of the song",
                inline=False,
            )
            embed.set_footer(text="Feel free to give me feedback!")
            return embed

        case _:
            return
