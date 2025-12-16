from redbot.core import commands, checks, Config
import discord

class MUtrix(commands.Cog):
    """MUtrix Merit Unit System"""

    def __init__(self, bot):
        self.bot = bot
        self.allowed_channel_id = 1450164417072336897  # Replace with your channel ID

        # JSON storage
        self.config = Config.get_conf(self, identifier=987654321012345678)
        default_member = {"mu": 0}
        self.config.register_member(**default_member)

    # Restrict commands to allowed channel
    async def cog_check(self, ctx):
        if ctx.channel.id != self.allowed_channel_id:
            await ctx.send(f"Sorry, MUtrix commands only work in <#{self.allowed_channel_id}>.")
            return False
        return True

    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        """Check MU balance for yourself or another member."""
        member = member or ctx.author
        mu = await self.config.member(member).mu()
        await ctx.send(f"{member.display_name} has {mu} MU.")

    @commands.command()
    @checks.admin()
    async def award(self, ctx, member: discord.Member, amount: int):
        """Award MU to a user."""
        current = await self.config.member(member).mu()
        await self.config.member(member).mu.set(current + amount)
        await ctx.send(f"{member.display_name} has been awarded {amount} MU. Total: {current + amount} MU.")

    @commands.command()
    @checks.admin()
    async def remove(self, ctx, member: discord.Member, amount: int):
        """Remove MU from a user."""
        current = await self.config.member(member).mu()
        new_total = max(current - amount, 0)
        await self.config.member(member).mu.set(new_total)
        await ctx.send(f"{amount} MU removed from {member.display_name}. Total: {new_total} MU.")

def setup(bot):
    bot.add_cog(MUtrix(bot))
