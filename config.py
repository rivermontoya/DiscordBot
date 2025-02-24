import asyncio
import discord
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
GENERAL_VC_ID = int(os.getenv("GENERAL_VC_ID"))
GENERAL_TEXT_CHAT = int(os.getenv("GENERAL_TEXT_CHAT"))

# Configure Discord Intents
intents = discord.Intents.default()

# Privileged Intents (Require enabling in Discord Developer Portal)
intents.members = True  # Access to member lists
intents.presences = True  # Access to user status (online, idle, etc.)
intents.message_content = True  # Access to message content

# Non-Privileged Intents
intents.guilds = True  # Enables guild-related events
intents.messages = True  # Enables message-related events (without content unless message_content is enabled)
intents.reactions = True  # Allows reaction-related events
intents.voice_states = True  # Allows tracking voice channel activity
intents.typing = True  # Allows tracking when users are typing
intents.integrations = True  # Allows access to integration events
intents.webhooks = True  # Allows access to webhook events
intents.invites = True  # Allows tracking invite-related events
intents.auto_moderation = True  # Allows access to auto-moderation events
intents.guild_scheduled_events = True  # Allows tracking scheduled events in a server
intents.bans = True  # Allows tracking banned members
intents.emojis = True  # Allows tracking emoji updates

# Expose module imports for other files
__all__ = ["asyncio", "discord", "requests", "TOKEN", "WEBHOOK_URL", "GENERAL_VC_ID", "GENERAL_TEXT_CHAT", "intents"]