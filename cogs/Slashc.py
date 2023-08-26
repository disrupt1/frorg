import discord
import random
from discord.ext import commands
from typing import Optional
from discord.ui import View, Button
from discord import app_commands

class Slashc(commands.Cog):
    """some shit"""
    def __init__(self, client):
        self.client = client
        

    @app_commands.command()
    async def clear(self, interaction: discord.Interaction, amount: int):
        """Clears the amount of messages given"""
        if interaction.user.guild_permissions.manage_channels == False:
            await interaction.response.send_message("You dont have permissions.")
        else:
            await interaction.response.defer(thinking=True, ephemeral=True)
            await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"Deleted {amount} message(s)", ephemeral=True)
            emb1 = discord.Embed(description=f"Deleted {amount} messages")
            emb1.set_footer(text=f"Invoked by {interaction.user.display_name}")
            await interaction.channel.send(embed=emb1)
    
    @app_commands.command()
    @app_commands.describe(member="Select the member.", nickname="Choose a nickname.")
    async def setnick(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        """Changes the nickname for a user in the server."""
        if interaction.user.guild_permissions.manage_nicknames == False:
            await interaction.response.send_message("You don't have permissions.", ephemeral=True)
        else:
            await member.edit(nick=nickname)
            await interaction.response.send_message(f"Changed nickname for {member.mention} to ({nickname})")
            
    @setnick.error
    async def setnick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("I can't update that user's nickname because they have a higher role than me.")
            
    @app_commands.command()
    @app_commands.describe(role="Select the role.", member="Select the member.")
    async def addrole(self, interaction: discord.Interaction, role: discord.Role, member: discord.Member):
        """Adds a role to selected member."""
        if interaction.user.guild_permissions.manage_roles == False:
            await interaction.response.send_message("You do not have Manage Roles permission to run this command.", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"Added {role.mention} to {member.mention}")
        
    @app_commands.command()
    @app_commands.describe(role="Select the role.", member="Select the member.")
    async def removerole(self, interaction: discord.Interaction, role: discord.Role, member: discord.Member):
        """Removes a role from selected member."""
        if interaction.user.guild_permissions.manage_roles == False:
            await interaction.response.send_message("You do not have Manage Roles permission to run this command.", ephemeral=True)
        else:
            await member.remove_roles(role)
            await interaction.response.send_message(f"Removed {role.mention} to {member.mention}")

    @app_commands.command()
    @app_commands.describe(member="Select a member to kick", reason="The reason why you want to kick this member.")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
        """ Kicks a user """
        if member.id == self.client.application_id:
            await interaction.response.send_message("what did i do")
        if interaction.user.guild_permissions.kick_members == False:
            await interaction.response.send_message("You don't have permission to run this command.", ephemeral=True)
        else:
            await member.kick(reason=reason)
            if member.bot == True:
                pass
            else:
                await member.send(f"You have been kicked from {interaction.guild} for: {reason}")
            emb = discord.Embed(description=f"Successfully kicked ({member.display_name}) out of the server", color=discord.Colour.random())
            await interaction.response.send_message(embed=emb)

    @app_commands.command()
    @app_commands.describe(member="Select a member to ban", reason="The reason why you want to ban this member.")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
        """ Bans a user """
        if interaction.user.guild_permissions.ban_members == False:
            await interaction.response.send_message("You dont have permission to run this command.", ephemeral=True)
        elif interaction.user.guild_permissions.ban_members:
            await member.ban(reason=reason)
            if member.bot == True:
                pass
            else:
                await member.send(f"You have been banned from {interaction.guild} for: {reason}")
            emb1 = discord.Embed(description=f"Successfully banned ({member.display_name}) from the server", color=discord.Colour.random())
            await interaction.response.defer()
            await interaction.followup.send(embed=emb1)
            
    @app_commands.command()
    @app_commands.describe(member="Select the member you want to mute.", reason="The reason why you want to mute this person. (optional)")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
        """Mute a member"""
        if interaction.user.guild_permissions.manage_roles == False:
            await interaction.response.send_message("You don't have Manage Roles permission to run this command.")
        else:
            muterole = discord.utils.get(interaction.guild.roles, name='Muted.')
            guild = interaction.guild
            if reason == None:
                reason = "No reason provided."
            if not muterole:
                await interaction.response.send_message("Mute role not detected. Creating mute role...", ephemeral=True)
                muterole = await guild.create_role(name='Muted.')
                for channel in guild.channels:
                    await channel.set_permissions(muterole, send_messages=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)
                await interaction.edit_original_response(content="Mute role has been created, run the command again.")
            else:
                await member.add_roles(muterole)
                await interaction.response.send_message(f"{member.mention} has been muted for: {reason}")
            
    @app_commands.command()
    @app_commands.describe(member="Select the member you want to unmute.")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        """Unmute a member"""
        if interaction.user.guild_permissions.manage_roles == False:
            await interaction.response.send_message("You don't have Manage Roles permission to run this command.")
        else:
            muterole = discord.utils.get(interaction.guild.roles, name='Muted.')
            if not muterole:
                await interaction.response.send_message("Member is not muted", ephemeral=True)
            else:
                await member.remove_roles(muterole)
                await interaction.response.send_message(f"{member.mention} has been unmuted.")

    @app_commands.command()
    @app_commands.describe(channel="Select the channel you want to lock (optional)")
    async def lock(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]):
        """Locks down the current channel"""
        if interaction.user.guild_permissions.manage_channels == False:
            await interaction.response.send_message("You don't have permission.", ephemeral=True)
        elif interaction.user.guild_permissions.manage_channels:
            if channel == None:
                overwritess = {
                    interaction.guild.default_role: discord.PermissionOverwrite(send_messages=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)
                }
                channell = interaction.channel
                await interaction.response.defer(thinking=True)
                await channell.edit(overwrites=overwritess)
                await interaction.followup.send("🔒Channel has been locked down.")
            else:
                overwritesdd = {
                    interaction.guild.default_role: discord.PermissionOverwrite(send_messages=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)
                }
                await interaction.response.defer(thinking=True)
                await channel.edit(overwrites=overwritesdd)
                await interaction.followup.send(f"🔒{channel.mention} Has been locked down.")

    @app_commands.command()
    @app_commands.describe(channel="Select the channel you want to unlock (optional)")
    async def unlock(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]):
        """Unlocks the current channel"""
        if interaction.user.guild_permissions.manage_channels == False:
            await interaction.response.send_message("You don't have permission.", ephemeral=True)
        elif interaction.user.guild_permissions.manage_channels:
            if channel == None:
                overwritess = {
                    interaction.guild.default_role: discord.PermissionOverwrite(send_messages=True, send_messages_in_threads=True, create_public_threads=True, create_private_threads=True)
                }
                channell = interaction.channel
                await interaction.response.defer(thinking=True)
                await channell.edit(overwrites=overwritess)
                await interaction.followup.send("🔓Channel has been unlocked.")
            else:
                overwritesdd = {
                    interaction.guild.default_role: discord.PermissionOverwrite(send_messages=True, send_messages_in_threads=True, create_public_threads=True, create_private_threads=True)
                }
                await interaction.response.defer(thinking=True)
                await channel.edit(overwrites=overwritesdd)
                await interaction.followup.send(f"🔓{channel.mention} Has been unlocked.")

    @app_commands.command()
    @app_commands.choices(choices=[app_commands.Choice(name="Heads", value="heads"), app_commands.Choice(name="Tails", value="tails")])
    async def coinflip(self, interaction: discord.Interaction, choices:app_commands.Choice[str]):
        """coinflipping test"""
        values = ["heads", "tails"]
        computerchoice = random.choice(values)
        if computerchoice == choices.value:
            await interaction.response.send_message("You chose the right option!")
        elif computerchoice != choices.value:
            await interaction.response.send_message("You chose the wrong option.")

async def setup(client):
    await client.add_cog(Slashc(client))