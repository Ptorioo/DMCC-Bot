from src.config import *
from youtubesearchpython import VideosSearch
import yt_dlp


class Music(commands.Cog):
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
                await ctx.send("Could not connect to voice channel.")
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
            coro = ctx.send(embed=message)
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
            coro = ctx.send("There are no songs to be played in the queue.")
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
            await ctx.send(embed=message)

            self.vc[id].play(
                discord.FFmpegPCMAudio(song["url"], **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx),
            )
        else:
            self.is_playing[id] = False
            self.duration[id] = []
            await ctx.send("There are no songs to be played in the queue.")

    def search(self, arg):
        videosSearch = VideosSearch(arg, limit=1)
        results = videosSearch.result()

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

    @commands.command()
    async def join(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
        elif self.vc[id] != None:
            if ctx.author.voice.channel != self.vc[id].channel:
                await ctx.send("Already joined a voice channel.")
            else:
                pass
        else:
            channel = ctx.author.voice.channel
            await self.joinVC(ctx, channel)

    @commands.command(name="leave", aliases=["dc", "disconnect"], help="")
    async def leave(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
        elif ctx.author.voice.channel != self.vc[id].channel:
            await ctx.send(
                "You need to be in the same voice channel to use this command."
            )
        elif self.vc[id] != None:
            self.is_playing[id] = self.is_paused[id] = False
            self.musicQueue[id] = []
            self.queueIndex[id] = 0
            self.duration[id] = []
            await self.vc[id].disconnect()
            self.vc[id] = None
            await ctx.send("Disconnected successfully.")
        else:
            return

    @commands.command(name="clear", aliases=["c"], help="")
    async def clear(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
        elif ctx.author.voice.channel != self.vc[id].channel:
            await ctx.send(
                "You need to be in the same voice channel to use this command."
            )
        else:
            if self.vc[id] != None and self.is_playing[id]:
                self.is_playing[id] = self.is_paused[id] = False
                self.vc[id].stop()
            if self.musicQueue[id] != []:
                await ctx.send("The music queue has been cleared.")
                self.musicQueue[id] = []
            self.queueIndex[id] = 0
            self.duration[id] = []

    @commands.command(name="pause", aliases=["stop"], help="")
    async def pause(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
        elif ctx.author.voice.channel != self.vc[id].channel:
            await ctx.send(
                "You need to be in the same voice channel to use this command."
            )
        elif self.is_playing[id]:
            self.is_playing[id] = False
            self.is_paused[id] = True
            self.vc[id].pause()
            await ctx.send("Music paused!")
        else:
            await ctx.send("Error handling number: 100001")

    @commands.command(name="resume", aliases=["r"], help="")
    async def resume(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
        elif ctx.author.voice.channel != self.vc[id].channel:
            await ctx.send(
                "You need to be in the same voice channel to use this command."
            )
        elif self.is_paused[id]:
            self.is_playing[id] = True
            self.is_paused[id] = False
            self.vc[id].resume()
            await ctx.send("The music is now playing!")
        else:
            await ctx.send("Error handling number: 100002")

    @commands.command(name="nowplaying", aliases=["np"], help="")
    async def nowplaying(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
        elif ctx.author.voice.channel != self.vc[id].channel:
            await ctx.send(
                "You need to be in the same voice channel to use this command."
            )
        elif self.is_playing[id]:
            song = self.musicQueue[id][self.queueIndex[id]][0]
            message = self.now_playing_embed(ctx, song)
            await ctx.send(embed=message)
        else:
            return

    @commands.command(name="skip", aliases=["s"], help="")
    async def skip(self, ctx):
        id = int(ctx.guild.id)
        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
        elif ctx.author.voice.channel != self.vc[id].channel:
            await ctx.send(
                "You need to be in the same voice channel to use this command."
            )
        elif self.queueIndex[id] == len(self.musicQueue[id]) - 1:
            self.vc[id].pause()
            self.queueIndex[id] += 1
            self.is_paused[id] = True
            self.is_playing[id] = False
            self.duration[id] = []
            await ctx.send("Song skipped, no more songs in the queue.")
        elif self.vc[id] and self.is_playing[id]:
            self.vc[id].pause()
            self.queueIndex[id] += 1
            await self.play_music(ctx)
            await ctx.send("Song skipped.")
        elif self.queueIndex[id] > len(self.musicQueue[id]) - 1:
            pass
        #            await ctx.send("Queue index out of range.")
        else:
            await ctx.send("Error handling number: 100003")

    @commands.command(name="queue", aliases=["q"], help="")
    async def queue(self, ctx):
        id = int(ctx.guild.id)
        returnValue = ""
        if self.musicQueue[id] == []:
            await ctx.send("There are no songs in the queue.")
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
                await ctx.send("There are no songs in the queue.")
                return
        queue = discord.Embed(
            title="Current Queue", description=returnValue, colour=0x00FF00
        )
        await ctx.send(embed=queue)

    @commands.command(name="play", aliases=["p"], help="")
    async def play(self, ctx, *args):
        id = int(ctx.guild.id)
        arg = " ".join(args)

        if not ctx.author.voice:
            await ctx.send("You are not in a voice channel.")
            return
        elif self.vc[id] != None:
            if ctx.author.voice.channel != self.vc[id].channel:
                await ctx.send(
                    "You need to be in the same voice channel to use this command."
                )
                return
            else:
                pass

        channel = ctx.author.voice.channel
        if not args:
            if len(self.musicQueue[id]) == 0:
                await ctx.send("There are no song to be played in the queue.")
                return
            elif not self.is_playing[id]:
                if len(self.musicQueue[id]) > 0:
                    await self.play_music(ctx)
                else:
                    return
            else:
                return
        else:
            song = self.search(arg)
            if type(song) == type(True):
                await ctx.send("Could not load the song.")
            else:
                self.musicQueue[id].append([song, channel, ctx.author])

                if not self.is_playing[id]:
                    await self.play_music(ctx)
                else:
                    await ctx.send("Added to queue.")


async def setup(bot):
    await bot.add_cog(Music(bot))
