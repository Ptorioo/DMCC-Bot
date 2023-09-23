from config import *

class DMCC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#TODO

async def setup(bot):
    await bot.add_cog(DMCC(bot))