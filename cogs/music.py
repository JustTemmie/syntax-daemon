import discord
from discord.ext import commands, tasks

import asyncio
import time
import random

import os


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.play_audio_task.start()

        self.common_sounds = []
        self.rare_sounds = []
        self.epic_sounds = []
        self.legendary_sounds = []
        
        for file in os.listdir("./assets/audio/common"):
            self.common_sounds.append(f"./assets/audio/common/{file}")
        
        for file in os.listdir("./assets/audio/rare"):
            self.rare_sounds.append(f"./assets/audio/rare/{file}")
        
        for file in os.listdir("./assets/audio/epic"):
            self.epic_sounds.append(f"./assets/audio/epic/{file}")

        for file in os.listdir("./assets/audio/legendary"):
            self.legendary_sounds.append(f"./assets/audio/legendary/{file}")

    # @commands.command(
    #     name="yup",
    #     brief="yup",
    #     description="yep mmhm",
    #     extras={"page": "main", "category":"music"}
    # )
    # async def yup(self, ctx):
    #     await self.play_the_yup(ctx.guild)
    
    # @commands.command(name="test")
    # async def test_audio(self, ctx: commands.Context):
    #     print(self.epic_sounds)
    #     song = random.choice(self.legendary_sounds)
    #     song = "assets/audio/legendary/NRK Dagsrevyen - New Intro (2015) [_Kuip3SSeCI].mp3"
    #     await self.play_sound(ctx.guild, song)
    
    async def play_sound(self, guild, sound):
        print(f"playing {sound} in {guild}")
        members: list[discord.Member] = []
        
        for voice_channel in guild.voice_channels:
            members += voice_channel.members
        
        if len(members) == 0:
            return

        user = random.choice(members)
        
        voice_client = await user.voice.channel.connect()

        await asyncio.sleep(1.5)

        audio_source = discord.FFmpegPCMAudio(sound)
        voice_client.play(audio_source, after=lambda e: self.bot.loop.create_task(self.disconnect_after_playing(voice_client)))

    async def disconnect_after_playing(self, voice_client):
        while voice_client.is_playing():
            await asyncio.sleep(0.1)
        
        voice_client.cleanup()
        await voice_client.disconnect()
    
    @tasks.loop(minutes=1)
    async def play_audio_task(self):
        for guild in self.bot.guilds:
            if random.random() > 0.99993:
                await self.play_sound(guild, random.choice(self.common_sounds))
            
            if random.random() > 0.99995:
                await self.play_sound(guild, random.choice(self.rare_sounds))
            
            if random.random() > 0.99997:
                await self.play_sound(guild, random.choice(self.epic_sounds))

            if random.random() > 0.999999:
                await self.play_sound(guild, random.choice(self.legendary_sounds))
        
async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
