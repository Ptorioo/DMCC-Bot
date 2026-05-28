import os
import random
import discord
import overpy
from shapely.geometry import Point, shape
from config import *

@app_commands.guilds(*sync_guilds)
class StreetView(commands.GroupCog, name="streetview", description = "play street view guessing"):
    def __init__(self, bot):
        self.bot = bot
        self.current_image = None
        self.current_coords = None

    @app_commands.command(
        name="streetview",
        description="View a street and guess its country with /streetview guess"
    )
    async def streetview(self, ctx):
        if not ctx.guild:
            return

        await self.send_random_image(ctx)


    @app_commands.command(
        name="guess",
        description="guess the country"
    )
    @app_commands.describe(
        country="name of the country"
    )
    async def guess(self, ctx, country:str):
        if not ctx.guild or not self.current_image or not self.current_coords:
            ctx.response.send_message("Use `/streetview streetview` to start first")
            return

        guessed_country = " ".join(country).lower()

        if self.is_correct_guess(guessed_country):
            await ctx.response.send_message("✅")
            await self.send_random_image(ctx, False)
        else:
            await ctx.response.send_message("❌")

    @app_commands.command(
        name="end",
        description="End the street view guessing"
    )
    async def stop(self, ctx):
        if not ctx.guild:
            return

        self.current_image = None
        self.current_coords = None
        await ctx.response.send_message("The street view guessing game has been ended.")

    async def send_random_image(self, ctx, commanded = True):
        folder_path = STREETVIEW_FOLDER
        
        try:
            random_image = random.choice(os.listdir(folder_path))
            while not os.path.isfile(os.path.join(folder_path, random_image)):
                random_image = random.choice(os.listdir(folder_path))
        except IndexError:
            if commanded:
                await ctx.response.send_message("No images found in the folder.")
            else:
                await ctx.channel.send("No images found in the folder.")
            return

        self.current_image = random_image
        try:
            lat_str, lng_str = random_image.rsplit('.', 1)[0].split('_')
            lat = float(lat_str.replace('_', '.'))
            lng = float(lng_str.replace('_', '.'))
        except ValueError:
            if commanded:
                await ctx.response.send_message("Invalid image filename format.")
            else:
                ctx.channel.send("Invalid image filename format.")
            return

        self.current_coords = Point(lng, lat)

        image_path = os.path.join(folder_path, random_image)

        embed = discord.Embed(title="Guess the Country", color=discord.Color.blue())
        file = discord.File(image_path, filename=random_image)
        embed.set_image(url=f"attachment://{random_image}")

        if commanded:
            await ctx.response.send_message(file=file, embed=embed)
        else:
            ctx.channel.send(file=file, embed=embed)

    def is_correct_guess(self, guessed_country):
        api = overpy.Overpass()
        query = f"""
        [out:json];
        is_in({self.current_coords.y}, {self.current_coords.x});
        area._[admin_level=2];
        out body;
        """
        try:
            result = api.query(query)
            for element in result.areas:
                if "name" in element.tags and element.tags["name"].lower() == guessed_country:
                    return True
                if "ISO3166-1:alpha2" in element.tags and element.tags["ISO3166-1:alpha2"].lower() == guessed_country:
                    return True
        except overpy.exception.OverpassException as e:
            print(f"Overpass API error: {e}")
        return False

async def setup(bot):
    await bot.add_cog(StreetView(bot))
