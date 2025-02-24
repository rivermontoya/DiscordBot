import random
import json
import asyncio
import os
from datetime import datetime, timedelta
from discord.ext import commands
from utils.self_destruct import send_self_destructing_message, attempt_deletion_on_startup  # Import logging utilities

BALANCE_FILE = "data/balances.json"

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances = self.load_balances()  # Load balances on startup
        self.bot.loop.create_task(attempt_deletion_on_startup(bot))  # Try deleting stored messages on startup

    def load_balances(self):
        """Loads user balances from a file."""
        try:
            with open(BALANCE_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Return empty dict if no file exists

    def save_balances(self):
        """Saves user balances to a file."""
        os.makedirs(os.path.dirname(BALANCE_FILE), exist_ok=True)  # Ensure directory exists
        with open(BALANCE_FILE, "w") as f:
            json.dump(self.balances, f, indent=4)

    @commands.command(name="balance")
    async def check_balance(self, ctx):
        """Checks user's balance."""
        balance = self.balances.get(str(ctx.author.id), 0)
        await send_self_destructing_message(ctx, f"{ctx.author.mention}, you have 💰 {balance} coins!")

    @commands.command(name="earn")
    async def earn_money(self, ctx):
        """Gives a random amount of coins."""
        amount = random.randint(5, 50)
        self.balances[str(ctx.author.id)] = self.balances.get(str(ctx.author.id), 0) + amount
        self.save_balances()  # Save to file after earning
        await send_self_destructing_message(ctx, f"🎉 {ctx.author.mention}, you earned 💰 {amount} coins!")

    @commands.command(name="gamble")
    async def gamble_money(self, ctx, amount: int):
        """Gambles coins for a chance to win double or lose everything."""
        balance = self.balances.get(str(ctx.author.id), 0)
        if amount > balance:
            await send_self_destructing_message(ctx, f"🚫 {ctx.author.mention}, you don't have enough coins!")
            return

        if random.choice([True, False]):
            self.balances[str(ctx.author.id)] += amount
            await send_self_destructing_message(ctx, f"🎉 {ctx.author.mention}, you won and now have 💰 {self.balances[str(ctx.author.id)]} coins!")
        else:
            self.balances[str(ctx.author.id)] -= amount
            await send_self_destructing_message(ctx, f"😢 {ctx.author.mention}, you lost! You now have 💰 {self.balances[str(ctx.author.id)]} coins.")

        self.save_balances()  # Save after gambling

async def setup(bot):
    await bot.add_cog(EconomyCog(bot))
