import requests
import random
import logging
from discord.ext import commands

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_welcome_message(self, member_name: str) -> str:
        try:
            headers = {"Accept": "application/json"}
            response = requests.get("https://icanhazdadjoke.com/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                joke = data.get('joke', 'Welcome to the voice chat!')
                logging.info(f"✅ Successfully fetched joke for {member_name}: {joke}")
                return f"😂 {member_name}, here's a joke for you: \"{joke}\""
            else:
                logging.warning(f"⚠️ API returned status {response.status_code}: {response.text}")

        except Exception as e:
            logging.error(f"❌ Error fetching joke for {member_name}: {e}", exc_info=True)

        # Fallback messages if API call fails
        fallback_messages = [
            f"🎤 {member_name} has entered the chat! Let's get this party started! 🕺",
            f"🎤 Welcome, {member_name}! Time to drop some wisdom in voice chat. 🎤",
            f"🎤 {member_name}, welcome aboard! 🚀"
        ]
        fallback_choice = random.choice(fallback_messages)
        logging.info(f"🔄 Using fallback message for {member_name}: {fallback_choice}")
        return fallback_choice

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
