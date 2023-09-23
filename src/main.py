from config import *
import status

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, owner_ids=set(OWNERS), intents=intents)

async def init():
    for cog_file in os.listdir(COG_DIR):
        if cog_file.endswith('.py'):
            await bot.load_extension(f'cog.{cog_file[:-3]}')

@bot.event
async def on_ready():
    bot.loop.create_task(status.renew(bot))
    logging.info(f"{bot.user.name} is now running!")

@bot.event
async def on_command_error(ctx, error):
    print(f"{ctx.guild.name}:  {error}")

@bot.command()
@commands.is_owner()
async def reload(ctx):
    for cog_file in os.listdir(COG_DIR):
        if cog_file.endswith('.py'):
            await bot.reload_extension(f'cog.{cog_file[:-3]}')
    logging.info(f"{bot.user.name} is now refreshed!")
    await ctx.send(f"{bot.user.name} is now refreshed!")

if __name__ == '__main__':
    asyncio.run(init())
    bot.run(TOKEN, root_logger=True)