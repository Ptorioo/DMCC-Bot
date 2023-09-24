from config import *

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx, *arg):
        if len(arg) == 0:
            response = get_response('help')
            await send_response(ctx, response, True)
        elif arg[0] == 'music':
            response = get_response('help-music')
            await send_response(ctx, response, True)
        elif arg[0] == 'quiz':
            response = get_response('help-quiz')
            await send_response(ctx, response, True)
        else:
            return

async def setup(bot):
    bot.remove_command('help')
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
        case 'help':
            embed = discord.Embed(
                title='Welcome to DMCC Bot!',
                description='I am a multi-purpose bot created by @lemniscape. \n Find out more about me by using the subcategory help commands listed below!',
                color=0x00ff00
            )
            embed.add_field(
                name='Music',
                value='`!help music` info about the music commands',
                inline=False
            )
#            embed.add_field(
#                name='Quiz',
#                value='`!help quiz` info about the geography quizzes',
#                inline=False
#            )
            embed.set_footer(text='Feel free to give me feedback!')
            return embed
        case 'help-quiz':
            embed = discord.Embed(
                title='Quiz',
                description='`!skip` skip the current question \n `!end` end the current quiz',
                color=0x00ff00
            )
            embed.add_field(
                name='Area Code Quizzes',
                value='`!code country` full list of countries available \n `!code *insert country*` quiz of requested country',
                inline=False
            )
            embed.add_field(
                name='Division Quizzes',
                value='`!div country` full list of countries available \n `!div *insert country*` quiz of requested country',
                inline=False
            )
            embed.add_field(
                name='Divisional Flag Quizzes',
                value='`!flag country` full list of countries available \n `!flag *insert country*` quiz of requested country',
                inline=False
            )
            embed.add_field(
                name='',
                value='You have 30 seconds to answer the question. \n The game ends automatically after two unanswered rounds.',
                inline=False
            )
            embed.set_footer(text='Feel free to give me feedback!')
            return embed
        case 'help-music':
            embed = discord.Embed(
                title='Music',
                description='',
                color=0x00ff00
            )
            embed.add_field(
                name='Clear',
                value='`!clear`, `!c` clear the current queue',
                inline=False
            )
            embed.add_field(
                name='Join',
                value='`!join` join the voice channel',
                inline=False
            )
            embed.add_field(
                name='Leave',
                value='`!leave`, `!disconnect` disconnect from the current voice channel',
                inline=False
            )
            embed.add_field(
                name='Pause',
                value='`!pause`, `!stop` pause the current queue',
                inline=False
            )
            embed.add_field(
                name='Play',
                value='`!play`,`!p` play the song given an url or search keyword',
                inline=False
            )
            embed.add_field(
                name='Queue',
                value='`!queue`, `!q` show the current queue',
                inline=False
            )
            embed.add_field(
                name='Resume',
                value='`!resume`, `!r` resume the current queue',
                inline=False
            )
            embed.add_field(
                name='Skip',
                value='`!skip`, `!s` skip the current song',
                inline=False
            )
            embed.set_footer(text='Feel free to give me feedback!')
            return embed
        case _:
            return