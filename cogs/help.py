from discord.ext import commands
import discord

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    async def custom_help(self, ctx, command_name: str = None):
        """Displays categorized help for commands."""
        
        # If a specific command is requested, show detailed info
        if command_name:
            command = self.bot.get_command(command_name)
            if command:
                embed = discord.Embed(
                    title=f"Help: {command.name}",
                    description=command.help or "No description provided.",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Usage", value=f"`!{command.name} {command.signature}`", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Command not found.")
            return

        # Otherwise, show categorized command help
        embed = discord.Embed(
            title="📜 Bot Command List",
            description="Use `!help <command>` for details on a specific command.",
            color=discord.Color.green()
        )

        # Group commands by cogs (categories)
        cogs = {}
        for cmd in self.bot.commands:
            if cmd.cog_name not in cogs:
                cogs[cmd.cog_name] = []
            cogs[cmd.cog_name].append(cmd)

        # Add categorized command list to embed
        for cog_name, commands in cogs.items():
            cmd_list = "\n".join([f"🔹 **{cmd.name}** - {cmd.help or 'No description'}" for cmd in commands])
            embed.add_field(name=f"🛠 {cog_name}", value=cmd_list, inline=False)

        # Send help via DM for better readability
        try:
            await ctx.author.send(embed=embed)
            await ctx.send("📩 Help menu sent via DM!")
        except discord.Forbidden:
            await ctx.send("❌ I can't send DMs. Please enable DMs to receive help.")

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
