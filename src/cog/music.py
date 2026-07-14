from config import *
from youtubesearchpython import VideosSearch
import yt_dlp

@app_commands.guilds(*sync_guilds)
class Music(commands.GroupCog, name="music", description = "play music via youtube"):
    def __init__(self, bot):
        self.bot = bot

        self.vc = {}
        self.is_paused = {}
        self.is_playing = {}
        self.musicQueue = {}
        self.queueIndex = {}
        self.duration = {}

        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M",
            "options": "-vn",
        }

        self.ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
            "quiet": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

    async def _init(self):
        for guild in self.bot.guilds:
            id = int(guild.id)
            self.vc[id] = None
            self.is_paused[id] = False
            self.is_playing[id] = False
            self.musicQueue[id] = []
            self.queueIndex[id] = 0
            self.duration[id] = []
        await self.on_time_update()

    async def _init_leave(self):
        for guild in self.bot.guilds:
            id = int(guild.id)
            if self.vc[id] != None:
                await self.vc[id].disconnect()
                self.vc[id] = None
            else:
                return

    async def joinVC(self, ctx, channel):
        id = int(ctx.guild.id)
        if self.vc[id] == None or not self.vc[id].is_connected():
            self.vc[id] = await channel.connect()
            await ctx.guild.change_voice_state(
                channel=channel, self_mute=False, self_deaf=True
            )

            if self.vc[id] == None:
                await ctx.response.send_message("Could not connect to voice channel.")
                return
        else:
            await self.vc[id].move_to(channel)
            await ctx.guild.change_voice_state(
                channel=channel, self_mute=False, self_deaf=True
            )

    def now_playing_embed(self, ctx, song):
        id = int(ctx.guild.id)
        title = song["title"]
        link = song["webpage_url"]
        thumbnail = song["thumbnail"]
        author = self.musicQueue[id][self.queueIndex[id]][2]
        avatar = author.avatar

        elapsed = self.duration[id][1] - self.duration[id][0]
        duration = self.duration[id][2]
        progress = round(20 * (elapsed / duration))
        m_e, s_e = divmod(int(elapsed), 60)
        m_d, s_d = divmod(duration, 60)

        embed = discord.Embed(
            title="Now Playing",
            description=f"[{title}]({link})",
            colour=0x00FF00,
        )

        embed.add_field(
            name="",
            value="`"
            + progress * "▬"
            + "🔘"
            + (20 - progress) * "▬"
            + "`"
            + f"   {m_e}:{s_e:0>2d} / {m_d}:{s_d:0>2d}",
            inline=False,
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f"Song added by: {str(author)}", icon_url=avatar)
        return embed

    def play_next(self, ctx):
        id = int(ctx.guild.id)
        if not self.is_playing[id]:
            return
        if self.queueIndex[id] + 1 < len(self.musicQueue[id]):
            self.queueIndex[id] += 1
            self.is_playing[id] = True

            song = self.musicQueue[id][self.queueIndex[id]][0]
            self.duration[id] = [time.time(), time.time(), song["duration"]]

            message = self.now_playing_embed(ctx, song)
            coro = ctx.channel.send(embed=message)
            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except:
                pass

            self.vc[id].play(
                discord.FFmpegPCMAudio(song["url"], **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx),
            )
        else:
            self.queueIndex[id] += 1
            self.is_playing[id] = False
            self.duration[id] = []
            coro = ctx.channel.send("There are no songs to be played in the queue.")
            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except:
                pass

    async def play_music(self, ctx):
        id = int(ctx.guild.id)
        if self.queueIndex[id] < len(self.musicQueue[id]):
            self.is_playing[id] = True
            self.is_paused[id] = False

            if self.vc[id] == None:
                await self.joinVC(ctx, self.musicQueue[id][self.queueIndex[id]][1])

            song = self.musicQueue[id][self.queueIndex[id]][0]
            self.duration[id] = [time.time(), time.time(), song["duration"]]

            message = self.now_playing_embed(ctx, song)
            await ctx.channel.send(embed=message)

            self.vc[id].play(
                discord.FFmpegPCMAudio(song["url"], **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx),
            )
        else:
            self.is_playing[id] = False
            self.duration[id] = []
            await ctx.channel.send("There are no songs to be played in the queue.")

    def search(self, arg):
        videosSearch = VideosSearch(arg, limit=1)
        results = videosSearch.result()
        print(results["result"][0])

        url = "https://www.youtube.com/watch?v=" + results["result"][0]["id"]

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            song = ydl.extract_info(url, download=False)
            return song

    async def on_time_update(self):
        while True:
            for guild in self.bot.guilds:
                id = int(guild.id)
                if not self.is_paused[id] and len(self.duration[id]) > 0:
                    self.duration[id][1] = time.time()
            await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_ready(self):
        await self._init()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        id = int(guild.id)
        self.vc[id] = None
        self.is_paused[id] = False
        self.is_playing[id] = False
        self.musicQueue[id] = []
        self.queueIndex[id] = 0
        self.duration[id] = []
        logging.info(f"Music cog initialized from joining a new server! ID: {id}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        id = int(guild.id)
        self.vc[id] = None
        self.is_paused[id] = False
        self.is_playing[id] = False
        self.musicQueue[id] = []
        self.queueIndex[id] = 0
        self.duration[id] = []
        logging.info(f"Music cog reset from leaving a server! ID: {id}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        id = int(member.guild.id)
        if not member.id == self.bot.user.id:
            return
        elif before.channel == None:
            if member.guild.me.guild_permissions.deafen_members:
                await member.edit(deafen=True)

            cooldownMinutes = 5
            time = 0

            while True:
                await asyncio.sleep(1)
                time += 1
                if self.is_playing[id] and not self.is_paused[id]:
                    time = 0
                if time >= cooldownMinutes * 60:
                    self.is_playing[id] = False
                    self.is_paused[id] = False
                    self.musicQueue[id] = []
                    self.queueIndex[id] = 0
                    self.duration[id] = []
                    await self.vc[id].disconnect()
                if self.vc[id] == None or not self.vc[id].is_connected():
                    break

    @app_commands.command(
        name="join",
        description="Join your VC"
    )
    async def join(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.user.voice:
            await ctx.response.send_message("You are not in a voice channel.")
        elif self.vc[id] != None:
            if ctx.user.voice.channel != self.vc[id].channel:
                await ctx.response.send_message("Already joined a voice channel.")
            else:
                pass
        else:
            channel = ctx.user.voice.channel
            await ctx.response.send_message("Successfully joined your voice channel.")
            await self.joinVC(ctx, channel)

    @app_commands.command(
        name="leave",
        description="Leave your VC"
    )
    async def leave(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.user.voice:
            await ctx.response.send_message("You are not in a voice channel.")
        elif ctx.user.voice.channel != self.vc[id].channel:
            await ctx.response.send_message(
                "You need to be in the same voice channel to use this command."
            )
        elif self.vc[id] != None:
            self.is_playing[id] = self.is_paused[id] = False
            self.musicQueue[id] = []
            self.queueIndex[id] = 0
            self.duration[id] = []
            await self.vc[id].disconnect()
            self.vc[id] = None
            await ctx.response.send_message("Disconnected successfully.")
        else:
            await ctx.response.send_message("Error handling number: 100001")

    @app_commands.command(
        name="clear",
        description="Clear the current queue"
    )
    async def clear(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.user.voice:
            await ctx.response.send_message("You are not in a voice channel.")
        elif ctx.user.voice.channel != self.vc[id].channel:
            await ctx.response.send_message(
                "You need to be in the same voice channel to use this command."
            )
        else:
            if self.vc[id] != None and self.is_playing[id]:
                self.is_playing[id] = self.is_paused[id] = False
                self.vc[id].stop()
            if self.musicQueue[id] != []:
                await ctx.response.send_message("The music queue has been cleared.")
                self.musicQueue[id] = []
            self.queueIndex[id] = 0
            self.duration[id] = []

    @app_commands.command(
        name="pause",
        description="Pause the current music"
    )
    async def pause(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.user.voice:
            await ctx.response.send_message("You are not in a voice channel.")
        elif ctx.user.voice.channel != self.vc[id].channel:
            await ctx.response.send_message(
                "You need to be in the same voice channel to use this command."
            )
        elif self.is_playing[id]:
            self.is_playing[id] = False
            self.is_paused[id] = True
            self.vc[id].pause()
            await ctx.response.send_message("Music paused!")
        else:
            await ctx.response.send_message("Error handling number: 100001")

    @app_commands.command(
        name="resume",
        description="Resume the current music"
    )
    async def resume(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.user.voice:
            await ctx.response.send_message("You are not in a voice channel.")
        elif ctx.user.voice.channel != self.vc[id].channel:
            await ctx.response.send_message(
                "You need to be in the same voice channel to use this command."
            )
        elif self.is_paused[id]:
            self.is_playing[id] = True
            self.is_paused[id] = False
            self.vc[id].resume()
            await ctx.response.send_message("The music is now playing!")
        else:
            await ctx.response.send_message("Error handling number: 100002")

    @app_commands.command(
        name="now_playing",
        description="Show the current status of the music"
    )
    async def nowplaying(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.user.voice:
            await ctx.response.send_message("You are not in a voice channel.")
        elif ctx.user.voice.channel != self.vc[id].channel:
            await ctx.response.send_message(
                "You need to be in the same voice channel to use this command."
            )
        elif self.is_playing[id]:
            song = self.musicQueue[id][self.queueIndex[id]][0]
            message = self.now_playing_embed(ctx, song)
            await ctx.response.send_message(embed=message)
        else:
            return

    @app_commands.command(
        name="skip",
        description="Skip to the next music"
    )
    async def skip(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.user.voice:
            await ctx.response.send_message("You are not in a voice channel.")
        elif ctx.user.voice.channel != self.vc[id].channel:
            await ctx.response.send_message(
                "You need to be in the same voice channel to use this command."
            )
        elif self.queueIndex[id] == len(self.musicQueue[id]) - 1:
            self.vc[id].pause()
            self.queueIndex[id] += 1
            self.is_paused[id] = True
            self.is_playing[id] = False
            self.duration[id] = []
            await ctx.response.send_message("Song skipped, no more songs in the queue.")
        elif self.vc[id] and self.is_playing[id]:
            self.vc[id].pause()
            self.queueIndex[id] += 1
            await self.play_music(ctx)
            await ctx.response.send_message("Song skipped.")
        elif self.queueIndex[id] > len(self.musicQueue[id]) - 1:
            pass
        #            await ctx.response.send_message("Queue index out of range.")
        else:
            await ctx.response.send_message("Error handling number: 100003")

    @app_commands.command(
        name="queue",
        description="Check the current queue"
    )
    async def queue(self, ctx):
        id = int(ctx.guild.id)
        returnValue = ""
        if self.musicQueue[id] == []:
            await ctx.response.send_message("There are no songs in the queue.")
            return
        for i in range(self.queueIndex[id], len(self.musicQueue[id])):
            upNextSongs = len(self.musicQueue[id]) - self.queueIndex[id]
            if i > 5 + upNextSongs:
                break
            returnIndex = i - self.queueIndex[id]
            if returnIndex == 0:
                returnIndex = "Playing - "
            else:
                returnIndex = "- "
            returnValue += f"{returnIndex}[{self.musicQueue[id][i][0]['title']}]({self.musicQueue[id][i][0]['webpage_url']})\n"
            if returnValue == "":
                await ctx.response.send_message("There are no songs in the queue.")
                return
        queue = discord.Embed(
            title="Current Queue", description=returnValue, colour=0x00FF00
        )
        await ctx.response.send_message(embed=queue)

    @app_commands.command(
        name="play",
        description="Add a music to the queue"
    )
    @app_commands.describe(
        music="link or keyword of the music"
    )
    async def play(self, ctx, music:str = ""):
        id = int(ctx.guild.id)
        arg = " ".join(music)

        if not ctx.user.voice:
            await ctx.response.send_message("You are not in a voice channel.")
            return
        elif self.vc[id] != None:
            if ctx.user.voice.channel != self.vc[id].channel:
                await ctx.response.send_message(
                    "You need to be in the same voice channel to use this command."
                )
                return
            else:
                pass

        channel = ctx.user.voice.channel
        await ctx.response.defer()
        if not music:
            if len(self.musicQueue[id]) == 0:
                await ctx.followup.send("There are no song to be played in the queue.")
                return
            elif not self.is_playing[id]:
                if len(self.musicQueue[id]) > 0:
                    await self.play_music(ctx)
                    await ctx.followup.send("The music is now playing!")
                else:
                    return
            else:
                return
        else:
            song = self.search(arg)
            if type(song) == type(True):
                await ctx.followup.send("Could not load the song.")
            else:
                self.musicQueue[id].append([song, channel, ctx.user])

                if not self.is_playing[id]:
                    await self.play_music(ctx)
                    await ctx.followup.send("The music is now playing!")
                else:
                    await ctx.followup.send("Added to queue.")


async def setup(bot):
    await bot.add_cog(Music(bot))
