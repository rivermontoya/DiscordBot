import logging
import os
from discord.ext import commands
import sys
import asyncio
from config import TOKEN, intents  # Import intents from config

sys.dont_write_bytecode = True

# Configure logging
logging.basicConfig(level=logging.INFO, format="\n%(asctime)s | %(levelname)s | %(message)s\n")

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Load cogs dynamically and format cog names in logs
async def load_cogs():
    cog_list = []
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog = f"cogs.{filename[:-3]}"
            cog_list.append(cog)
            await bot.load_extension(cog)
    logging.info("\n🔄 Loaded Cogs:\n" + "\n".join(f"  - {cog}" for cog in cog_list) + "\n")

# Run bot
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    logging.info(f'\n✅ Bot is online as {bot.user}!\n')
    for guild in bot.guilds:
        logging.info(f"✅ Preparing to cache members for {guild.name}...")
        try:
            await asyncio.sleep(1)  # Prevents overloading the event loop
            await guild.chunk()
            logging.info(f"✅ Cached all members for {guild.name}\n")
        except Exception as e:
            logging.warning(f"⚠️ Could not chunk {guild.name}: {e}")
    asyncio.create_task(read_terminal_commands(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Process commands
    await bot.process_commands(message)

    # Delete the message if it is a command
    if message.content.startswith(bot.command_prefix):
        async def delete_message_later():
            await asyncio.sleep(10)  # Set self-destruct timer
            try:
                await message.delete()
            except Exception:
                pass  # Message may have already been deleted manually

        asyncio.create_task(delete_message_later())

async def read_terminal_commands(bot):
    """Reads commands from the terminal and processes them asynchronously."""
    loop = asyncio.get_running_loop()
    while True:
        command = await asyncio.to_thread(input, "Enter command: ")  # Runs input() in a separate thread
        if command == "stop":
            await bot.close()
            break
        elif command.startswith("!"):
            if bot.guilds:
                system_channel = bot.guilds[0].system_channel
                if system_channel:
                    ctx = await bot.get_context(await system_channel.send(command))
                    await bot.invoke(ctx)
                else:
                    print("System channel not found.")
            else:
                print("No guilds available.")
        else:
            print("Unknown command. Use '!' prefix for bot commands or 'stop' to terminate.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("\n🛑 Bot terminated via CTRL+C\n")
