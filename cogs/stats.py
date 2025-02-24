import logging
from discord.ext import commands, tasks
import discord
from datetime import datetime, timedelta
from config import GENERAL_TEXT_CHAT
from utils.self_destruct import save_stats_message_id, load_stats_message_id

class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_stats_message_id = load_stats_message_id()  # Load the last stats message ID on startup
        self.post_server_stats.start()

    @tasks.loop(minutes=60)
    async def post_server_stats(self):
        """Posts detailed server statistics in a specific text channel between 5PM and Midnight Eastern Time."""
        current_utc = datetime.utcnow()
        eastern_hour = (current_utc - timedelta(hours=5)).hour  # Convert UTC to Eastern manually
        if 17 <= eastern_hour < 24:  # 5PM to 11:59PM Eastern Time
            await self.send_server_stats()
        else:
            logging.info("⏳ Skipping server stats post - Outside of active hours (5PM - Midnight ET)")

    @commands.command(name="serverstats")
    async def manual_server_stats(self, context):
        """Allows users to manually request server stats."""
        await self.send_server_stats(context.channel)

    async def send_server_stats(self, channel=None):
        """Gathers and sends server stats to a specified channel."""
        logging.info("\n📊 Attempting to post server stats...\n")
        if channel is None:
            channel = self.bot.get_channel(GENERAL_TEXT_CHAT)
        
        if not channel:
            logging.warning(f"⚠️ Channel with ID {GENERAL_TEXT_CHAT} not found.\n")
            return

        guild = channel.guild
        if not guild:
            logging.warning("⚠️ Channel does not belong to a guild.\n")
            return

        await guild.chunk()
        members = guild.members
        total_members = guild.member_count
        bots = sum(1 for member in members if member.bot)
        humans = total_members - bots

        online_members = sum(1 for member in members if member.status == discord.Status.online)
        offline_members = sum(1 for member in members if member.status == discord.Status.offline)
        dnd_members = sum(1 for member in members if member.status == discord.Status.dnd)
        idle_members = sum(1 for member in members if member.status == discord.Status.idle)

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        roles_count = len(guild.roles)
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count
        server_owner = guild.owner
        server_creation = guild.created_at.strftime("%Y-%m-%d")

        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        eastern_time = (datetime.utcnow() - timedelta(hours=5)).strftime("%Y-%m-%d %I:%M %p ET")

        stats_message = (
            "\n📊 **Server Stats:**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"🏠 **Server Name:** `{guild.name}`\n"
            f"👑 **Owner:** {server_owner.mention}\n"
            f"📅 **Created On:** `{server_creation}`\n"
            f"⏰ **Current Time:** `{current_time} / {eastern_time}`\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"👥 **Members:** `{total_members}` (Humans: `{humans}`, Bots: `{bots}`)\n"
            f"🟢 Online: `{online_members}` | 🌙 Idle: `{idle_members}` | 🔴 DND: `{dnd_members}` | ⚫ Offline: `{offline_members}`\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"💬 **Text Channels:** `{text_channels}` | 🔊 **Voice Channels:** `{voice_channels}`\n"
            f"🎭 **Roles:** `{roles_count}`\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"💎 **Boost Level:** `{boost_level}` (Boosts: `{boost_count}`)\n"
            "━━━━━━━━━━━━━━━━━━━\n"
        )

        logging.info(f"\n✅ Posting server stats: \n{stats_message}\n")
        
        if self.last_stats_message_id:
            try:
                last_message = await channel.fetch_message(self.last_stats_message_id)
                await last_message.delete()
                logging.info("✅ Deleted old server stats message.")
            except discord.NotFound:
                logging.warning("⚠️ Previous stats message not found. Posting new one.")

        message = await channel.send(stats_message)
        self.last_stats_message_id = message.id
        save_stats_message_id(self.last_stats_message_id)  # Save the new stats message ID

    @post_server_stats.before_loop
    async def before_post_server_stats(self):
        """Ensures the bot is ready before posting stats."""
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(StatsCog(bot))
