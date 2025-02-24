import asyncio
import json
from datetime import datetime
from collections import defaultdict

SELF_DESTRUCT_FILE = "data/self_destruct.json"
STATS_MESSAGE_FILE = "data/stats_message.json"
self_destruct_tasks = defaultdict(list)

async def attempt_deletion_on_startup(bot):
    """Attempts to delete any pending self-destruct messages stored in the file."""
    try:
        with open(SELF_DESTRUCT_FILE, "r") as f:
            data = json.load(f)
        
        for user_id, messages in data.items():
            for msg_id, timestamp in messages:
                try:
                    channel = bot.get_channel(msg_id[1])  # Assuming channel ID is stored alongside msg_id
                    if channel:
                        msg = await channel.fetch_message(msg_id[0])
                        await msg.delete()
                except Exception:
                    pass  # Message may no longer exist
        
        # After attempting deletions, clear the file
        open(SELF_DESTRUCT_FILE, "w").close()
    except (FileNotFoundError, json.JSONDecodeError):
        pass

async def send_self_destructing_message(ctx, message, seconds=10):
    """Sends a message that deletes itself after a set time."""
    msg = await ctx.send(message)
    timestamp = datetime.utcnow()
    self_destruct_tasks[str(ctx.author.id)].append((msg.id, ctx.channel.id, timestamp.isoformat()))
    save_self_destruct_data()

    async def delete_messages():
        await asyncio.sleep(seconds)
        try:
            await msg.delete()
        except Exception:
            pass  # Message may have already been deleted manually
        self_destruct_tasks[str(ctx.author.id)].remove((msg.id, ctx.channel.id, timestamp.isoformat()))
        save_self_destruct_data()

    asyncio.create_task(delete_messages())

def save_self_destruct_data():
    """Saves self-destruct data to a file."""
    with open(SELF_DESTRUCT_FILE, "w") as f:
        json.dump(self_destruct_tasks, f, indent=4)

def save_stats_message_id(message_id):
    """Saves the stats message ID to a file."""
    with open(STATS_MESSAGE_FILE, "w") as f:
        json.dump({"last_stats_message_id": message_id}, f, indent=4)

def load_stats_message_id():
    """Loads the stats message ID from a file."""
    try:
        with open(STATS_MESSAGE_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_stats_message_id")
    except (FileNotFoundError, json.JSONDecodeError):
        return None
