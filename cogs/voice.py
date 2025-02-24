import logging
from discord.ext import commands
import discord
from config import GENERAL_VC_ID
import asyncio

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join")
    async def join_voice(self, ctx):
        """Joins a voice channel or moves if already connected."""
        channel = self.bot.get_channel(GENERAL_VC_ID)

        if not channel:
            await ctx.send("❌ Voice channel not found.")
            return

        voice_client = ctx.voice_client  # Get the bot's current voice connection

        if voice_client:
            if voice_client.channel == channel:
                await ctx.send("🔊 I'm already in the target voice channel.")
                return
            await voice_client.disconnect()
            await voice_client.move_to(channel)
            msg = f"🔄 Moved bot to {channel.name}!"
        else:
            try:
                await channel.connect(timeout=10, reconnect=True)
                msg = f"✅ Joined {channel.name}!"
            except asyncio.TimeoutError:
                msg = "⚠️ Connection to voice channel timed out."
                logging.warning(msg)
                await ctx.send(msg)
                return
            except discord.errors.ClientException as e:
                msg = f"❌ Unable to join voice: {e}"
                logging.error(msg)
                await ctx.send(msg)
                return

        logging.info(msg)
        await ctx.send(msg)

    @commands.command(name="leave")
    async def leave_voice(self, ctx):
        """Leaves the voice channel if connected."""
        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()
            msg = "🚪 Bot has left the voice channel."
        else:
            msg = "❌ I'm not in a voice channel."

        logging.info(msg)
        await ctx.send(msg)

async def setup(bot):
    """Adds the VoiceCog to the bot dynamically."""
    await bot.add_cog(VoiceCog(bot))
