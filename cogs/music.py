import discord
from discord.ext import commands, tasks

import asyncio
import time
import random

demons = [
    "/home/twig/Personal/discord-bots/syntax-daemon/assets/audio/nooo.wav.mp3",
    "/home/twig/Personal/discord-bots/syntax-daemon/assets/audio/nopeimplayingwithmacock.wav.mp3",
    "/home/twig/Personal/discord-bots/syntax-daemon/assets/audio/nopeimplayingwithmyrod.wav.mp3",
    "/home/twig/Personal/discord-bots/syntax-daemon/assets/audio/yeeeuup.wav.mp3",
    "/home/twig/Personal/discord-bots/syntax-daemon/assets/audio/yep.wav.mp3",
    "/home/twig/Personal/discord-bots/syntax-daemon/assets/audio/yip.wav.mp3",
]

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.play_audio_task.start()
    

    @commands.command(
        name="yup",
        brief="yup",
        description="yep mmhm",
        extras={"page": "main", "category":"music"}
    )
    async def yup(self, ctx):
        await self.play_the_yup(ctx.guild)
    
    async def play_the_yup(self, guild):
        members: list[discord.Member] = []

        for voice_channel in guild.voice_channels:
            members += voice_channel.members
        
        if len(members) == 0:
            return
        
        user = random.choice(members)
        track = random.choice(demons)
        
        voice_client = await user.voice.channel.connect()

        audio_source = discord.FFmpegPCMAudio(track)
        voice_client.play(audio_source, after=lambda e: self.bot.loop.create_task(self.disconnect_after_playing(voice_client)))

    async def disconnect_after_playing(self, voice_client):
        while voice_client.is_playing():
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(1)

        await voice_client.disconnect()
    
    @tasks.loop(minutes=1)
    async def play_audio_task(self):
        for guild in self.bot.guilds:
            if random.random() > 0.996:
                await self.play_the_yup(guild)
        
async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
