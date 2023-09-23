from config import *

async def renew(bot):
    while True:
        await bot.change_presence(activity=discord.Game(name="🍕 Eating pizza..."))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game(name="🍹 Drinking smoothies..."))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game(name="👋 Greetings from Nishikata..."))
        await asyncio.sleep(15)