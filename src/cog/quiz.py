from config import *

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def div(self, ctx, arg):
        match arg:
            case 'country':
                response = get_response('quiz-div')
                await send_response(ctx, response, True)
            case _:
                return

    @commands.command()
    async def flag(self, ctx, arg):
        match arg:
            case 'country':
                response = get_response('quiz-flag')
                await send_response(ctx, response, True)
            case _:
                return

    @commands.command()
    async def code(self, ctx, arg):
        match arg:
            case 'country':
                response = get_response('quiz-code')
                await send_response(ctx, response, True)
            case _:
                return

async def setup(bot):
    await bot.add_cog(Quiz(bot))

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
        case 'quiz-div':
            embed = discord.Embed(title='Division Quizzes', description='- France', color=0x00ff00)
            embed.set_footer(text='Feel free to give me feedback!')
            return embed
        case 'quiz-flag':
            embed = discord.Embed(title='Divisional Flag Quizzes', description='- France', color=0x00ff00)
            embed.set_footer(text='Feel free to give me feedback!')
            return embed
        case 'quiz-code':
            embed = discord.Embed(title='Area Code Quizzes', description='- France', color=0x00ff00)
            embed.set_footer(text='Feel free to give me feedback!')
            return embed
        case _:
            return