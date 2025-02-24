import logging
from discord.ext import commands
from config import GENERAL_VC_ID

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Handles when a member's voice state changes."""
        general_channel = self.bot.get_channel(GENERAL_VC_ID)

        if not general_channel:
            logging.warning("❌ GENERAL_VC_ID is invalid or the channel does not exist.")
            return

        # Member joins the general voice channel
        if after.channel == general_channel and before.channel != general_channel:
            welcome_cog = self.bot.get_cog("WelcomeCog")
            if welcome_cog:
                welcome_message = welcome_cog.get_welcome_message(member.name)
                system_channel = general_channel.guild.system_channel

                if system_channel:  # Ensure system channel exists before sending
                    await system_channel.send(welcome_message)
                else:
                    logging.warning("⚠️ System channel not set for this server.")
            else:
                logging.error("❌ WelcomeCog not found.")

    @commands.Cog.listener()
    async def on_disconnect(self):
        """Logs when the bot disconnects."""
        logging.warning("⚠️ Bot has disconnected from the gateway. Attempting to reconnect...")

async def setup(bot):
    """Adds the cog to the bot."""
    await bot.add_cog(EventsCog(bot))
