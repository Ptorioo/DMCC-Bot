from config import *


class DMCC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, role, *args):
        next_line = False
        if role.lower() == "everyone":
            role_mention = "@everyone"
            next_line = True
        elif role.lower() == "here":
            role_mention = "@here"
            next_line = True
        else:
            try:
                role_object = discord.utils.get(ctx.guild.roles, name=role)
                role_mention = role_object.mention
            except AttributeError:
                role_mention = role

        arg = " ".join(args)
        await ctx.send(f"{role_mention}" + next_line * "\n" + f" {arg}")


# TODO


async def setup(bot):
    await bot.add_cog(DMCC(bot))
