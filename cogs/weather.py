import logging
import requests
from discord.ext import commands
import discord

class WorkingTestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="weather")
    async def fetch_weather(self, context):
        """Fetches the current weather for multiple locations using wttr.in API."""
        locations = [
            "Chicago, Illinois",
            "Grand Rapids, Michigan",
            "Houston, Texas",
            "New Jersey",
            "Pigeon Forge, Tennessee",
            "Traverse City, Michigan"
        ]
        
        weather_results = []
        for location in locations:
            url = f"https://wttr.in/{location}?format=%C+%t"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    weather_info = response.text.strip()
                    weather_results.append(f"🌡️ **{location}**: {weather_info}")
                else:
                    weather_results.append(f"⚠️ **{location}**: Unable to fetch weather data.")
            except Exception as e:
                logging.error(f"Error fetching weather for {location}: {e}")
                weather_results.append(f"❌ **{location}**: Failed to fetch weather.")
        
        await context.send("\n".join(weather_results))

async def setup(bot):
    await bot.add_cog(WorkingTestCog(bot))
