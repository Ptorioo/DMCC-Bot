from config import *

staff_role = int(STAFF_ROLE)
former_staff_role = int(FORMER_STAFF_ROLE)
member_role = int(MEMBER_ROLE)
life_member_role = int(LIFE_MEMBER_ROLE)

@app_commands.guilds(*sync_guilds)
class Staff(commands.GroupCog, name="staff", description = "commands for staffs"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="inherit",
        description="Delete all the members, only use it in new school year"
    )
    async def inherit(self, ctx):
        await ctx.response.defer()
        ganbu = ctx.guild.get_role(staff_role)
        cganbu = ctx.guild.get_role(former_staff_role)
        if ganbu in ctx.user.roles or cganbu.user.roles:
            mr = ctx.guild.get_role(member_role)
            lmr = ctx.guild.get_role(life_member_role)
            mrs = mr.members
            for mem in mrs:
                rrs = mem.roles
                if not (lmr in rrs or ganbu in rrs):
                    await mem.remove_roles(mr)
            for mem in lmr.members:
                if not mr in mem.roles:
                    await mem.add_roles(mr)
            #await ctx.response.send_message("換代完成")
            await ctx.followup.send("Inheritage completed")
        else:
            await ctx.followup.send("Command failed, please be a staff at least once to use this command.")



async def setup(bot):
    await bot.add_cog(Staff(bot))