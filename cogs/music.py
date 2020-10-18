import discord
import os
from discord.ext import commands
from discord.utils import get
import youtube_dl


class music_system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["J", "jo"])
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)

        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)

        else:
            voice = await channel.connect()
            print(f"The bot has connected to {channel}\n")

        await ctx.send(f"Joined {channel}")

    @commands.command(pass_context=True, aliases=["L", "le"])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has left {channel}")
            await ctx.send(f"Disconnected from {channel}")

        else:
            print("Bot was told to leave voice channel, yet was not in one")
            await ctx.send("Not in a current voice channel")

    @commands.command(pass_context=True, aliases=["p", "pl"])
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")

        except PermissionError:
            print("Trying to remove song file but it is being played")
            await ctx.send("Error")
            return

        await ctx.send("Ready Time")

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading Audio\n")

            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith("mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(
            discord.FFmpegPCMAudio("song.mp3"),
            after=lambda e: print(f"{name} has finished playing"),
        )
        voice.source = discord.PCVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname}")
        print("Playing")

    @commands.command(pass_context=True, aliases=["pa", "pau"])
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music Puase")
            voice.pause()
            await ctx.send("Music Paused")
        else:
            print("No Audio Playing")
            await ctx.send("Music is not playing, pause failure")

    @commands.command(pass_context=True, aliases=["re", "resum"])
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("Music Resume")
            voice.resume()
            await ctx.send("Music Resumed")
        else:
            print("No Audio Playing")
            await ctx.send("Music is not playing, resume failure")

    @commands.command(pass_context=True, aliases=["st", "stp"])
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print("Music Stopped")
            voice.stop()
            await ctx.send("Music Stopped")
        else:
            print("No Audio Playing")
            await ctx.send("Music is not playing, stop failure")


def setup(bot):
    bot.add_cog(music_system(bot))
