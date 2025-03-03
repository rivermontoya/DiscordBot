import discord
from discord.ext import commands
import logging

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join")
    async def join_voice(self, ctx):
        """Joins the voice channel of the user who ran the command."""
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("❌ You need to be in a voice channel for me to join.")
            return

        channel = ctx.author.voice.channel
        if ctx.voice_client:  # If bot is already connected
            if ctx.voice_client.channel == channel:
                await ctx.send("✅ I'm already in your voice channel.")
                return
            await ctx.voice_client.move_to(channel)
            await ctx.send(f"🔄 Moved to {channel.name}!")
        else:
            try:
                await channel.connect()
                await ctx.send(f"✅ Joined {channel.name}!")
            except Exception as e:
                logging.error(f"Error joining voice: {e}")
                await ctx.send("❌ Failed to join voice channel.")

    @commands.command(name="leave")
    async def leave_voice(self, ctx):
        """Leaves the current voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("🚪 Left the voice channel.")
        else:
            await ctx.send("❌ I'm not in a voice channel.")

async def setup(bot):
    await bot.add_cog(VoiceCog(bot))
