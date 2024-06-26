import status
from config import *

intents = discord.Intents.all()
owner_ids = set(map(int, OWNERS.split(',')))
bot = commands.Bot(command_prefix=PREFIX, owner_ids=owner_ids, intents=intents)

async def init():
    for cog_file in os.listdir('src/cog'):
        if cog_file.endswith(".py"):
            await bot.load_extension(f"cog.{cog_file[:-3]}")


@bot.event
async def on_ready():
    bot.loop.create_task(status.renew(bot))
    logging.info(f"{bot.user.name} is now running!")


@bot.event
async def on_command_error(ctx, error):
    if ctx.guild:
        logging.info(f"{ctx.guild.name}:  {error}")


@bot.command()
@commands.is_owner()
async def reload(ctx):
    if bot.get_cog("Music"):
        await bot.get_cog("Music")._init_leave()
    for cog_file in os.listdir('src/cog'):
        if cog_file.endswith(".py"):
            await bot.reload_extension(f"cog.{cog_file[:-3]}")
    logging.info(f"{bot.user.name} is now reloaded!")
    await ctx.send(f"{bot.user.name} is now reloaded!")
    await bot.get_cog("Music")._init()


if __name__ == "__main__":
    asyncio.run(init())
    bot.run(TOKEN, root_logger=True)
