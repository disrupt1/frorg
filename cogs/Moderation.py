import discord
from discord.ui import Button, View
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason='No reason provided.'):
        """ kicks a user """
        if ctx.author.id == member.id:
            await ctx.send("if you wanna kick yourself just leave the server bro")
        else:
            await member.kick(reason=reason)
            await member.send(f"You have been kicked from {ctx.guild} for: {reason}")
            emb = discord.Embed(description=f"Successfully kicked {member.display_name} out of the server", color=discord.Colour.random())
            await ctx.send(embed=emb)
            
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(error)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx: commands.Context):
        channelor = ctx.message.channel
        overwritess = {ctx.author.guild.default_role: discord.PermissionOverwrite(send_messages=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)}
        await channelor.edit(overwrites=overwritess)
        await ctx.send(f"{channelor.mention} Locked down.")
        
    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(error)
            
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx: commands.Context, member: discord.Member):
        muterole = discord.utils.get(ctx.guild.roles, name='Muted.')
        if not muterole:
            await ctx.send("Mute role not detected. Creating mute role...")
            muterole = await ctx.guild.create_role(name='Muted.')
            for channel in ctx.guild.channels:
                await channel.set_permissions(muterole, send_messages=False)
        await member.add_roles(muterole)
        await ctx.send(f"{member.mention} has been muted.")
        
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(error)
        
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member):
        muterole = discord.utils.get(ctx.guild.roles, name='Muted')
        if not muterole:
            await ctx.send("Member is not muted.")
        else:
            await member.remove_roles(muterole)
            await ctx.send(f"{member.mention} has been unmuted.")
            
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(error)

    @commands.command()
    async def unlock(self, ctx: commands.Context):
        if ctx.author.guild_permissions.manage_channels == False:
            await ctx.send("You do not have permissions.")
        elif ctx.author.guild_permissions.manage_guild:
            channelor = ctx.message.channel
            overwritess = {ctx.author.guild.default_role: discord.PermissionOverwrite(send_messages=True, send_messages_in_threads=True, create_public_threads=True, create_private_threads=True)}
            await channelor.edit(overwrites=overwritess)
            await ctx.send("channel unlocked")
            
    @commands.command()
    async def setnick(self, ctx: commands.Context, member: discord.Member, nickname: str):
        """Changes the nickname for a user in the server."""
        if ctx.author.guild_permissions.manage_nicknames == False:
            await ctx.send("You don't have permissions.")
        elif ctx.author.guild_permissions.manage_nicknames:
            await member.edit(nick=nickname)
            await ctx.send(f"Changed nickname for {member.mention} to ({nickname})")
        
    @commands.command()
    async def clear(self, ctx: commands.Context, amount: int):
        """Clears the amount of messages given"""
        await ctx.channel.purge(limit=amount)
        emb1 = discord.Embed(description=f"Deleted {amount} messages", color=discord.Colour.random())
        emb1.set_footer(text=f"Invoked by {ctx.author.display_name}")
        await ctx.channel.send(embed=emb1)
    
    @commands.command()
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason='No reason provided.'):
        """ bans a user """
        if ctx.author.id == member.id:
            await ctx.reply("if you wanna ban yourself just leave the server bro")
        elif ctx.author.guild_permissions.kick_members == False:
            await ctx.send("You dont have permission to run this command.")
        elif ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await member.send(f"You have been banned from {ctx.guild} for: {reason}")
            emb = discord.Embed(description=f"Successfully kicked {member.display_name} out of the server", color=discord.Colour.random())
            await ctx.send(embed=emb)

async def setup(client):
	await client.add_cog(Moderation(client))