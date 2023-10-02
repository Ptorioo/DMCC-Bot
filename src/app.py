import src.status
from src.config import *
from flask import Flask
from threading import Thread

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, owner_ids=set(OWNERS), intents=intents)


async def init():
    for cog_file in os.listdir('src/cog'):
        if cog_file.endswith(".py"):
            await bot.load_extension(f"cog.{cog_file[:-3]}")


@bot.event
async def on_ready():
    bot.loop.create_task(src.status.renew(bot))
    logging.info(f"{bot.user.name} is now running!")


@bot.event
async def on_command_error(ctx, error):
    if ctx.guild:
        print(f"{ctx.guild.name}:  {error}")


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

app = Flask('__name__')

@app.route('/')
def home():
    return "Server is up and running!"

def keep_alive():
    t = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8080})
    t.start()

if __name__ == "__main__":
    keep_alive()
    asyncio.run(init())
    bot.run(TOKEN, root_logger=True)
