import discord
from discord.ext import commands

class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        """bot's latency"""
        emb = discord.Embed(title="🏓", description=f"Bot's latency: {round(self.client.latency * 1000)}ms")
        await ctx.send(embed=emb)

    @commands.hybrid_command()
    async def serverinfo(self, ctx: commands.Context):
        """Shows information about the current server"""
        emb = discord.Embed(title="Information about this server.", description=f"This shows information about {ctx.guild.name}")
        emb.set_thumbnail(url=ctx.guild.icon)
        emb.add_field(name="🆔Server ID:", value=f"{ctx.guild.id}")
        emb.add_field(name="👥Members:", value=f"{ctx.guild.member_count} members")
        emb.add_field(name="💬Channels:", value=f"{len(ctx.guild.text_channels)} text | {len(ctx.guild.voice_channels)} voice")
        emb.add_field(name="🔒Roles:", value=f"{len(ctx.guild.roles)}")
        emb.add_field(name="❓Description:", value=f"{ctx.guild.description}")
        await ctx.send(embed=emb)
    
async def setup(client):
    await client.add_cog(Tools(client))